import logging
import os

from dialogflow import detect_intent_texts
from dotenv import load_dotenv
from google.auth import exceptions as google_exceptions
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from tg_logging import MyLogsHandler


def start(update, context):
    update.message.reply_text("Здравствуйте")


def send_answer(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    project_id = os.getenv("PROJECT_ID")
    try:
        dialogflow_response = detect_intent_texts(chat_id, message, project_id)
        update.message.reply_text(dialogflow_response.query_result.fulfillment_text)
    except google_exceptions.DefaultCredentialsError:
        logger.exception('Не удалось подключиться в dialogflow по запросу из телеграма (скорее всего неверно указан путь к json-файлу в .env)')


def main():
    bot_token = os.getenv("BOT_TOKEN")
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, send_answer))

    logger.info("Телеграм бот запущен")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    load_dotenv()

    logger = logging.getLogger("TG_Logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())

    main()
