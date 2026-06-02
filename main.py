import os

from persona import BuddyAI
from ui import ChatUI


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "buddy_ai_persona.csv")

    if os.path.exists(csv_path):
        bot = BuddyAI(csv_path)
    else:
        bot = BuddyAI()

    ui = ChatUI(bot)
    ui.run()


if __name__ == "__main__":
    main()
