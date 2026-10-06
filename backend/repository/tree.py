from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
}


def build_file_tree(repository_path: str | Path) -> list[str]:
    """
    Build a relative file tree for a repository.

    Ignored directories such as .git, venv and node_modules
    are excluded.
    """

    repository_path = Path(repository_path).resolve()

    if not repository_path.exists():
        raise FileNotFoundError(
            f"Repository does not exist: {repository_path}"
        )

    if not repository_path.is_dir():
        raise NotADirectoryError(
            f"Repository path is not a directory: {repository_path}"
        )

    file_tree = []

    for path in sorted(repository_path.rglob("*")):

        relative_path = path.relative_to(repository_path)

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        if path.is_file():
            file_tree.append(str(relative_path))

    return file_tree