from framework import detect_frameworks


REPOSITORY_PATH = "test_workspace/Hello-World"


def main():
    try:
        frameworks = detect_frameworks(REPOSITORY_PATH)

        print("\nDetected Frameworks:")
        print("-" * 40)

        if frameworks:
            for framework in frameworks:
                print(framework)
        else:
            print("No recognized frameworks found.")

        print("-" * 40)

    except Exception as error:
        print(f"\nFramework detection failed: {error}")


if __name__ == "__main__":
    main()