import logging
from auth import TOKEN
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


def first_response(update, context):
    # Сохраняем ответ в словаре.
    context.user_data['locality'] = update.message.text
    update.message.reply_text(
        f"Какая погода в городе {context.user_data['locality']}?")
    return 2


# Добавили словарь user_data в параметры.
def second_response(update, context):
    weather = update.message.text
    logger.info(weather)
    # Используем user_data в ответе.
    update.message.reply_text(
        f"Спасибо за участие в опросе! Привет, {context.user_data['locality']}!")
    context.user_data.clear()  # очищаем словарь с пользовательскими данными
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text & ~Filters.command, first_response, pass_user_data=True)],
            # ...и для его использования.
            2: [MessageHandler(Filters.text & ~Filters.command, second_response, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("first_response", first_response))
    dp.add_handler(CommandHandler("second_response", second_response))
    dp.add_handler(CommandHandler("stop", stop))
    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()