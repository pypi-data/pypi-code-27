from . import (
    call_black,
    parse_black_result,
    calculate_percentage,
    generate_badge,
    logger,
)
import sys

VERSION = "0.0.3"


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("Usage: black-percentage-test")
        print("\nOptions:")
        print("    --generate-badge    Generate shield.io badge with calculated value.")
        exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] == "--version":
        print(f"black-percentage-test {VERSION}")
        exit(1)

    black_result = call_black()
    logger.debug(f"black_result={black_result}")
    changed, unchanged = parse_black_result(black_result)
    percentage = calculate_percentage(changed, unchanged)

    print(f"Your project is \033[91m{percentage}%\033[0m formatted by black!")

    if len(sys.argv) == 2 and sys.argv[1] == "--generate-badge":
        badge_url = generate_badge(percentage)
        print(f"Here is your badge: \033[90m{badge_url}\033[0m")


if __name__ == "__main__":
    main()
