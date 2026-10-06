from pathlib import Path


EXTENSION_TO_LANGUAGE = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".kt": "Kotlin",
    ".swift": "Swift",
}


def detect_languages(repository_path: str | Path) -> dict[str, int]:
    """
    Detect programming languages used in a repository.

    Returns:
        Dictionary containing language names and file counts.
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

    language_counts: dict[str, int] = {}

    for path in repository_path.rglob("*"):

        if not path.is_file():
            continue

        if any(
            part in {
                ".git",
                "__pycache__",
                ".venv",
                "venv",
                "node_modules",
            }
            for part in path.relative_to(repository_path).parts
        ):
            continue

        language = EXTENSION_TO_LANGUAGE.get(
            path.suffix.lower()
        )

        if language:
            language_counts[language] = (
                language_counts.get(language, 0) + 1
            )

    return language_counts