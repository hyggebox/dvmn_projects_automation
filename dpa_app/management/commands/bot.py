import logging
import os

import telegram

from dotenv import load_dotenv
from time import sleep
from telegram import Update
from telegram.ext import (CallbackContext, Updater, CommandHandler)

from django.utils import timezone
from django.core.management.base import BaseCommand
from dpa_app.models import Student, SendDate


BASIC_URL = 'https://automatizationprojects.herokuapp.com/'
SLEEP_TIME_FOR_MSG_RESEND = 7200  # in seconds


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown(
        f'Привет, {user.full_name}!\n'
        f'Позже пришлю тебе ссылку на форму, '
        f'где ты сможешь выбрать удобное время для созвона 😊\n\n'
    )


def send_link(bot, user_id, deadline):
    msg = f'🔔 Пройди по ссылке и выбери удобные для созвона слоты: {BASIC_URL}{user_id}\n\n' \
          f'Заполнить форму нужно до {deadline.strftime("%d.%m %H:%M")} (МСК)'
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

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    now = timezone.now()
    links_send_date = SendDate.objects.filter(title__contains='формы').get()
    start_link_send = links_send_date.start_at
    end_link_send = links_send_date.end_at

    result_send_date = SendDate.objects.filter(title__contains='Результаты').get()
    start_result_send = result_send_date.start_at
    end_result_send = result_send_date.end_at
    while True:
        if start_link_send and end_link_send and \
                start_link_send <= now < end_link_send and 9 <= now.hour:
            for user_id in db_user_ids:
                student = Student.objects.get(tg_id=user_id)
                if not student.link_sent:
                    try:
                        send_link(bot, user_id, end_link_send)
                        student.link_sent = True
                        student.save()
                        logging.info(f'Message sent to user with id {user_id}')
                    except telegram.error.BadRequest:
                        logging.error(f'Message cannot be sent to user with id {user_id}')

        if start_result_send and end_result_send and \
                start_result_send <= now < end_result_send and 9 <= now.hour:
            for user_id in db_user_ids:
                student = Student.objects.get(tg_id=user_id)
                if not student.result_sent:
                    try:
                        send_result(bot, user_id)
                        student.result_sent = True
                        student.save()
                        logging.info(f'Message sent to user with id {user_id}')
                    except Student.DoesNotExist:
                        logging.error(f'Student with id {user_id} not found in the database')
                    except ValueError:
                        logging.error(f"Student with id {user_id} doesn't belong to any group")
                    except telegram.error.BadRequest:
                        logging.error(f'Message cannot be sent to user with id {user_id}')
        sleep(SLEEP_TIME_FOR_MSG_RESEND)


    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()


class Command(BaseCommand):
    # Start the bot.

    help = "Телеграм-бот"
    main()

