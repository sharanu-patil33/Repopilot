from pathlib import Path


CONFIG_FILES = {
    "requirements.txt": "Python dependencies",
    "pyproject.toml": "Python project configuration",
    "setup.py": "Python package configuration",
    "package.json": "Node.js project configuration",
    "package-lock.json": "Node.js dependency lock file",
    "yarn.lock": "Yarn dependency lock file",
    "pnpm-lock.yaml": "pnpm dependency lock file",
    "Dockerfile": "Docker configuration",
    "docker-compose.yml": "Docker Compose configuration",
    "docker-compose.yaml": "Docker Compose configuration",
    ".env.example": "Environment variable template",
    "pom.xml": "Maven configuration",
    "build.gradle": "Gradle configuration",
    "build.gradle.kts": "Gradle Kotlin configuration",
    "Makefile": "Make build configuration",
}


IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
}


def detect_config_files(
    repository_path: str | Path,
) -> dict[str, str]:
    """
    Recursively detect important configuration files
    inside a repository.

    Returns:
        Dictionary mapping relative file paths
        to their configuration purpose.
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

    detected = {}

    for path in repository_path.rglob("*"):

        if not path.is_file():
            continue

        relative_path = path.relative_to(repository_path)

        # Ignore generated/dependency directories.
        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        filename = path.name

        if filename in CONFIG_FILES:
            detected[str(relative_path)] = CONFIG_FILES[filename]

    return dict(sorted(detected.items()))