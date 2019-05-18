import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from bot import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.LOG_LEVEL),
)
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "Hello. How can I help you? A loan maybe?\n\n"
            "If you're not sure type /help for the available command list."
        ),
    )


def help(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=("/start - show greeting message\n" "/help - show command list"),
    )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "Sorry, I didn't understand that command. "
            "Try /help to see the list of available commands."
        ),
    )


def error(update, context):
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def main():
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
