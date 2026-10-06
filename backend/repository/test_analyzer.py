import json

from analyzer import analyze_repository


REPOSITORY_PATH = "test_workspace/Hello-World"


def main():
    try:
        report = analyze_repository(REPOSITORY_PATH)

        print("\nRepository Analysis Report:")
        print("=" * 60)

        print(
            json.dumps(
                report,
                indent=4
            )
        )

        print("=" * 60)

    except Exception as error:
        print(f"\nRepository analysis failed: {error}")


if __name__ == "__main__":
    main()