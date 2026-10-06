from pathlib import Path


FRAMEWORK_FILES = {
    "manage.py": "Django",
    "angular.json": "Angular",
    "next.config.js": "Next.js",
    "next.config.mjs": "Next.js",
    "vite.config.js": "Vite",
    "vite.config.ts": "Vite",
    "pom.xml": "Maven",
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


def detect_frameworks(repository_path: str | Path) -> list[str]:
    """
    Recursively detect frameworks and major project tools
    inside a repository.
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

    detected = set()

    for path in repository_path.rglob("*"):

        if not path.is_file():
            continue

        relative_path = path.relative_to(repository_path)

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        filename = path.name

        # Framework-specific files
        if filename in FRAMEWORK_FILES:
            detected.add(FRAMEWORK_FILES[filename])

        # Python dependency files
        if filename == "requirements.txt":
            content = path.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "fastapi" in content:
                detected.add("FastAPI")

            if "flask" in content:
                detected.add("Flask")

            if "django" in content:
                detected.add("Django")

        # Node.js package files
        if filename == "package.json":
            content = path.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if '"react"' in content:
                detected.add("React")

            if '"express"' in content:
                detected.add("Express")

            if '"next"' in content:
                detected.add("Next.js")

            if '"vite"' in content:
                detected.add("Vite")

    return sorted(detected)