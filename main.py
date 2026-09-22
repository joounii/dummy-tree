from dataclasses import asdict

from generator import generate_test_environment
from gui import get_config_ui


def main() -> None:
    config = get_config_ui()

    if not config:
        print("User closed the window without submitting.")
        return

    if config.verbose:
        print("[VERBOSE] User submitted configuration:")
        for key, val in asdict(config).items():
            print(f"  {key}: {val}")

    results = generate_test_environment(config)

    if config.verbose:
        print(f"[VERBOSE] Generation summary: {results}")


if __name__ == "__main__":
    main()