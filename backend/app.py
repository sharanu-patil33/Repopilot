from pathlib import Path

from repository.cloner import (
    clone_repository,
    RepositoryCloneError,
)
from repository.analyzer import analyze_repository


WORKSPACE = Path("workspace")


def analyze_github_repository(repo_url: str) -> tuple[dict, bool]:
    """
    Prepare and analyze a GitHub repository.

    Returns:
        report: Repository analysis report.
        cloned: True if newly cloned, False if reused.
    """

    repo_url = repo_url.strip()

    if not repo_url:
        raise ValueError(
            "Repository URL cannot be empty."
        )

    repository_name = repo_url.rstrip("/").split("/")[-1]

    if repository_name.endswith(".git"):
        repository_name = repository_name[:-4]

    repository_path = (
        WORKSPACE.resolve() / repository_name
    )

    was_existing = repository_path.exists()

    repository_path = clone_repository(
        repo_url,
        WORKSPACE,
    )

    report = analyze_repository(repository_path)

    return report, not was_existing


def print_report(report: dict) -> None:
    """
    Display the repository analysis.
    """

    print("\n")
    print("=" * 70)
    print("                 REPOPILOT REPOSITORY STATUS")
    print("=" * 70)

    print(f"\nRepository : {report['repository']}")
    print(f"Location   : {report['path']}")
    print(f"File Count : {report['file_count']}")

    print("\nLanguages")
    print("-" * 70)

    if report["languages"]:
        for language, count in report["languages"].items():
            print(f"  {language}: {count} file(s)")
    else:
        print("  No recognized programming languages found.")

    print("\nFrameworks / Tools")
    print("-" * 70)

    if report["frameworks"]:
        for framework in report["frameworks"]:
            print(f"  {framework}")
    else:
        print("  No recognized frameworks found.")

    print("\nConfiguration Files")
    print("-" * 70)

    if report["configuration_files"]:
        for filename, description in (
            report["configuration_files"].items()
        ):
            print(f"  {filename} -> {description}")
    else:
        print("  No recognized configuration files found.")

    print("\nFile Tree")
    print("-" * 70)

    for file in report["files"]:
        print(f"  {file}")

    print("\n" + "=" * 70)
    print("             Repository analysis completed")
    print("=" * 70)


def main():
    print("\n" + "=" * 70)
    print("                    REPOPILOT")
    print("=" * 70)

    print("\nEnter a public GitHub repository URL.")
    print(
        "Example: "
        "https://github.com/octocat/Hello-World.git"
    )

    repo_url = input(
        "\nGitHub Repository URL: "
    ).strip()

    try:
        print("\n[1/2] Preparing repository...")

        report, cloned = analyze_github_repository(
            repo_url
        )

        if cloned:
            print("Repository cloned successfully.")
        else:
            print("Existing repository reused.")

        print("[2/2] Analyzing repository...")

        print_report(report)

    except RepositoryCloneError as error:
        print(f"\nRepository Error: {error}")

    except Exception as error:
        print(f"\nUnexpected Error: {error}")


if __name__ == "__main__":
    main()