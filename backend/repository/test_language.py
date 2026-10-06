from language import detect_languages


REPOSITORY_PATH = "test_workspace/Hello-World"


def main():
    try:
        languages = detect_languages(REPOSITORY_PATH)

        print("\nDetected Languages:")
        print("-" * 40)

        if languages:
            for language, count in languages.items():
                print(f"{language}: {count} file(s)")
        else:
            print("No recognized programming languages found.")

        print("-" * 40)

    except Exception as error:
        print(f"\nLanguage detection failed: {error}")


if __name__ == "__main__":
    main()