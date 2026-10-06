from config import detect_config_files


REPOSITORY_PATH = "test_workspace/Hello-World"


def main():
    try:
        configs = detect_config_files(REPOSITORY_PATH)

        print("\nDetected Configuration Files:")
        print("-" * 40)

        if configs:
            for filename, description in configs.items():
                print(f"{filename} -> {description}")
        else:
            print("No recognized configuration files found.")

        print("-" * 40)

    except Exception as error:
        print(f"\nConfiguration detection failed: {error}")


if __name__ == "__main__":
    main()