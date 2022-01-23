import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dvmn_projects_automation.settings")

import django
django.setup()

import logging
import os

import telegram

from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, Updater, CommandHandler)

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from dpa_app.models import TimeSlot, PM, Group, Student


BASIC_URL = 'https://automatizationprojects.herokuapp.com/'


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown(
        f'Привет, {user.full_name}\!\n'
        f'Позже пришлю тебе ссылку на форму, '
        f'где ты сможешь выбрать удобное время для созвона 😊\n\n'
    )


def send_link(bot, user_id):
    msg = f'🔔 Пройди по ссылке и выбери удобные для созвона слоты: {BASIC_URL}{user_id}\n\n' \
          f'Заполнить форму нужно до <25.01 18:00 (МСК)>'
    bot.sendMessage(chat_id=user_id, text=msg)


def send_result(bot, user_id):
    student = Student.objects.get(tg_id=user_id)
    students_group = student.group
    if students_group:
        groups_time_slot = str(students_group.time_slot)
        groups_pm = students_group.pm.name
        fellow_students = students_group.students.all()
        fellow_students_names = [f'{student.f_name} {student.l_name}' for student in fellow_students]

        msg = f'Группы распределены! 🎉\n\n' \
              f'⏰ Время созвона: {groups_time_slot}\n' \
              f'👤 Твой ПМ: {groups_pm}\n' \
              f'👥 Твоя группа:\n'
        for student_name in fellow_students_names:
            msg += f'{student_name}\n'
        bot.sendMessage(chat_id=user_id, text=msg)
    else:
        raise ValueError


def main() -> None:
    """Start the bot."""
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')

    logging.basicConfig(
        format='%(levelname)s: %(asctime)s - %(name)s - %(message)s',
        level=logging.INFO)

    db_students = Student.objects.all()
    db_user_ids = [student.tg_id for student in db_students]
    # db_user_ids = [123, 802604339]  # for testing

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    utc_now = datetime.utcnow()
    start_date_for_send = 1
    end_date_for_send = 3
    if start_date_for_send <= utc_now.day < end_date_for_send and 6 <= utc_now.hour <= 11:
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
            except Student.DoesNotExist:
                logging.error(f'Student with id {user_id} not found in the database')
            except ValueError:
                logging.error(f"Student with id {user_id} doesn't belong to any group")
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

