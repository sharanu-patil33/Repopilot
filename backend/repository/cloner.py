from pathlib import Path
import subprocess
from urllib.parse import urlparse


class RepositoryCloneError(Exception):
    """Raised when a repository cannot be cloned."""
    pass


def validate_repository_url(repo_url: str) -> None:
    """
    Validate that the provided URL is a GitHub HTTP/HTTPS URL.
    """

    if not repo_url or not repo_url.strip():
        raise RepositoryCloneError(
            "Repository URL cannot be empty."
        )

    repo_url = repo_url.strip()

    parsed = urlparse(repo_url)

    if parsed.scheme not in {"http", "https"}:
        raise RepositoryCloneError(
            "Repository URL must use HTTP or HTTPS."
        )

    if parsed.netloc.lower() not in {
        "github.com",
        "www.github.com",
    }:
        raise RepositoryCloneError(
            "Only GitHub repositories are supported."
        )


def get_repository_name(repo_url: str) -> str:
    """
    Extract the repository name from a GitHub URL.
    """

    path = urlparse(repo_url).path.strip("/")

    if not path:
        raise RepositoryCloneError(
            "Could not determine repository name from URL."
        )

    repository_name = path.split("/")[-1]

    if repository_name.endswith(".git"):
        repository_name = repository_name[:-4]

    if not repository_name:
        raise RepositoryCloneError(
            "Could not determine repository name from URL."
        )

    return repository_name


def clone_repository(
    repo_url: str,
    workspace: str | Path,
) -> Path:
    """
    Clone a GitHub repository into the given workspace.

    If the repository already exists in the workspace,
    the existing repository is reused.

    Returns:
        Path to the repository.
    """

    validate_repository_url(repo_url)

    workspace_path = Path(workspace).resolve()
    workspace_path.mkdir(parents=True, exist_ok=True)

    repository_name = get_repository_name(repo_url)
    repository_path = workspace_path / repository_name

    # Reuse an existing repository.
    if repository_path.exists():

        if not repository_path.is_dir():
            raise RepositoryCloneError(
                f"Repository path exists but is not a directory: "
                f"{repository_path}"
            )

        # Make sure it actually looks like a Git repository.
        if not (repository_path / ".git").exists():
            raise RepositoryCloneError(
                f"Directory already exists but is not a Git repository: "
                f"{repository_path}"
            )

        return repository_path

    command = [
        "git",
        "clone",
        "--depth",
        "1",
        repo_url,
        str(repository_path),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
        )

    except subprocess.TimeoutExpired as exc:
        raise RepositoryCloneError(
            "Repository cloning timed out."
        ) from exc

    except FileNotFoundError as exc:
        raise RepositoryCloneError(
            "Git was not found. Please install Git and make sure "
            "it is available in PATH."
        ) from exc

    if result.returncode != 0:
        error_message = result.stderr.strip()

        if not error_message:
            error_message = "Unknown Git error."

        raise RepositoryCloneError(
            f"Failed to clone repository: {error_message}"
        )

    return repository_path