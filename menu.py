"""Simple game selection menu."""

from __future__ import annotations


def main() -> None:
    while True:
        print()
        print("Select a game:")
        print("1) Snake")
        print("2) Mini Doom")
        print("3) Jira Chatbot")
        print("4) Quit")
        choice = input("Enter choice [1-4]: ").strip()
        if choice == "1":
            from snake import main as snake_main
            snake_main()
        elif choice == "2":
            from doom import main as doom_main
            doom_main()
        elif choice == "3":
            from jira_bot import main as jira_main
            jira_main()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
