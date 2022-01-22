import logging
import os

import telegram

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, Updater, CommandHandler)

from django.core.management.base import BaseCommand
from dpa_app.models import TimeSlot, PM, Group, Student


BASIC_URL = 'https://automatizationprojects.herokuapp.com/'


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Привет, {user.full_name}\!\n'
        f'Позже пришлю тебе ссылку на форму, '
        f'где ты сможешь выбрать удобное время для созвона 😊\n\n'
    )


def send_link(bot, user_id):
    msg = f'🔔 Пройди по ссылке и выбери удобные для созвона слоты: {BASIC_URL}{user_id}\n\n' \
          f'Заполнить форму нужно до <25.01 18:00 (МСК)>'
    bot.sendMessage(chat_id=user_id, text=msg)


def send_result(bot, user_id):
    msg = 'Группы распределены! 🎉\n\n' \
          '⏰ Время созвона: {19:00-19:30}\n' \
          '👤 Твой ПМ: {Имя ПМа}\n' \
          '👥 Твоя группа:\n-- {Имя 1}\n-- {Имя 2}\n-- {Имя 3}'
    bot.sendMessage(chat_id=user_id, text=msg)


def main() -> None:
    """Start the bot."""
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')

    logging.basicConfig(
        format='%(levelname)s: %(asctime)s - %(name)s - %(message)s',
        level=logging.INFO)

    db_students = Student.objects.all()
    db_user_ids = [student.tg_id for student in db_students]
    # db_user_ids = [12, 802604339, 123]  # for testing

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))


    if False: # Заменить на условие, при котором будет отправляться ссылка на форму
        for user_id in db_user_ids:
            try:
                send_link(bot, user_id)
                logging.info(f'Message sent to user with id {user_id}')
            except telegram.error.BadRequest:
                logging.error(f'Message cannot be sent to user with id {user_id}')


    if False: # Заменить на условие, когда будет отправляться результат
        for user_id in db_user_ids:
            try:
                send_result(bot, user_id)
                logging.info(f'Message sent to user with id {user_id}')
            except telegram.error.BadRequest:
                logging.error(f'Message cannot be sent to user with id {user_id}')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


class Command(BaseCommand):
    # Start the bot.

    help = "Телеграм-бот"
    main()

