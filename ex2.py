import logging
import random

from telegram import ReplyKeyboardMarkup

from auth import TOKEN
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/dice', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

dice_keyboard = [['/one_cub', '/two_cubs'],
                 ['/very_big_cub', '/back']]
markup_dice = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)

timer_keyboard = [['/thirty_seconds', "/one_minute"],
                  ['/two_minutes', '/back']]
timer_dice = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True



def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text='КУКУ!')



def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def start(update, context):
    update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup
    )


def dice(update, context):
    update.message.reply_text(
        "какой кубик бросить?",
        reply_markup=markup_dice
    )


def timer(update, context):
    update.message.reply_text(
        "какой таймер задать?",
        reply_markup=timer_dice
    )



def thirty_seconds(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = 30
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')



def one_minute(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = 60
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

        text = f'Вернусь через 1 минуту!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def two_minutes(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = 120
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

        text = f'Вернусь через 2 минуты!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')



def one_cub(update, context):
    a = random.randint(1, 6)
    update.message.reply_text(a)


def two_cubs(update, context):
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    c = str(a) + ' ' + str(b)
    update.message.reply_text(c)


def very_big_cub(update, context):
    a = random.randint(1, 20)
    update.message.reply_text(a)


def back(update, context):
    update.message.reply_text(
        'Вернулся на предыдущую',
        reply_markup=markup
    )


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("one_cub", one_cub))
    dp.add_handler(CommandHandler("two_cubs", two_cubs))
    dp.add_handler(CommandHandler("very_big_cub", very_big_cub))
    dp.add_handler(CommandHandler("back", back))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("one_minute", one_minute))
    dp.add_handler(CommandHandler("thirty_seconds", thirty_seconds))
    dp.add_handler(CommandHandler("two_minutes", two_minutes))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()