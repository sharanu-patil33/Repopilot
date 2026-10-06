from pathlib import Path

from cloner import clone_repository
from analyzer import analyze_repository


REPOSITORY_URL = "https://github.com/octocat/Hello-World.git"
WORKSPACE = Path("test_workspace")


def main():
    try:
        print("\n[1] Cloning repository...")
        
        repository_path = clone_repository(
            REPOSITORY_URL,
            WORKSPACE,
        )

        print(f"Repository cloned to: {repository_path}")

        print("\n[2] Analyzing repository...")

        report = analyze_repository(repository_path)

        print("\n[3] Repository Status")
        print("=" * 60)

        print(f"Repository : {report['repository']}")
        print(f"Files      : {report['file_count']}")
        print(f"Languages  : {report['languages']}")
        print(f"Frameworks : {report['frameworks']}")
        print(
            f"Config     : "
            f"{report['configuration_files']}"
        )

        print("=" * 60)

        print("\nRepository analysis completed successfully.")

    except Exception as error:
        print(f"\nRepository analysis failed: {error}")


if __name__ == "__main__":
    main()