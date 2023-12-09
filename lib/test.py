from telegram import Bot
from utils import get_all_posts
import os


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def main():
    # Initialize the Telegram Bot
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="test")


if __name__ == "__main__":
    main()
