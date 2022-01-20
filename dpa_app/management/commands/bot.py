import logging
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import (Filters, CallbackContext, Updater,
                          CommandHandler, MessageHandler)

from django.core.management.base import BaseCommand
from dpa_app.models import TimeSlot, PM, Group, Student


BASIC_URL = 'https://automatizationprojects\.herokuapp\.com/'


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Привет, {user.full_name}\!\n'
        f'Я пришлю тебе ссылку на форму, '
        f'где ты сможешь выбрать удобное время для созвона 😊\n\n'
        f'Ссылка: {BASIC_URL}{user.id}'
    )


def main() -> None:
    """Start the bot."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logger = logging.getLogger(__name__)

    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')

    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


class Command(BaseCommand):
    # Start the bot.

    help = "Телеграм-бот"
    main()

