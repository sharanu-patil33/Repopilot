from tree import build_file_tree


REPOSITORY_PATH = "test_workspace/Hello-World"


def main():
    try:
        files = build_file_tree(REPOSITORY_PATH)

        print("\nRepository File Tree:")
        print("-" * 40)

        for file in files:
            print(file)

        print("-" * 40)
        print(f"Total files: {len(files)}")

    except Exception as error:
        print(f"\nTree generation failed: {error}")


if __name__ == "__main__":
    main()