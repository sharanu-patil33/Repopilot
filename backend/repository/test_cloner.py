from pathlib import Path

from cloner import clone_repository, RepositoryCloneError


TEST_REPOSITORY = "https://github.com/octocat/Hello-World.git"


def main():
    workspace = Path("test_workspace")

    try:
        cloned_path = clone_repository(
            TEST_REPOSITORY,
            workspace,
        )

        print("\nRepository cloned successfully!")
        print(f"Location: {cloned_path}")

        if cloned_path.exists():
            print("Repository directory: OK")
        else:
            print("Repository directory: NOT FOUND")

    except RepositoryCloneError as error:
        print(f"\nClone failed: {error}")


if __name__ == "__main__":
    main()