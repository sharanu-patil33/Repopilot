from pathlib import Path

from .tree import build_file_tree
from .language import detect_languages
from .framework import detect_frameworks
from .config import detect_config_files


def analyze_repository(repository_path: str | Path) -> dict:
    """
    Perform a complete repository comprehension analysis.

    Combines:
    - File tree
    - Language detection
    - Framework detection
    - Configuration file detection
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

    files = build_file_tree(repository_path)
    languages = detect_languages(repository_path)
    frameworks = detect_frameworks(repository_path)
    configuration_files = detect_config_files(repository_path)

    return {
        "repository": repository_path.name,
        "path": str(repository_path),
        "file_count": len(files),
        "files": files,
        "languages": languages,
        "frameworks": frameworks,
        "configuration_files": configuration_files,
    }