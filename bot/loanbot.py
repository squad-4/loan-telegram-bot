import logging
from enum import Enum, auto

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from bot import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.LOG_LEVEL),
)
logger = logging.getLogger(__name__)


class LoanState(Enum):
    GETCLIENT = auto()


def start(update, context):
    update.message.reply_text(
        (
            "Hello. How can I help you? A loan maybe?\n"
            "If you're not sure type /help for the available command list."
        )
    )


def help(update, context):
    update.message.reply_text(
        (
            "/start - show greeting message\n"
            "/loan - create a loan\n"
            "/cancel - cancel current operation\n"
            "/help - show command list"
        )
    )


def unknown(update, context):
    update.message.reply_text(
        (
            "Sorry, I didn't understand that command.\n"
            "Try /help to see the list of available commands."
        )
    )


def error(update, context):
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def loan(update, context):
    update.message.reply_text("Please, send me your CPF number.")
    return LoanState.GETCLIENT


def get_client(update, context):
    update.message.reply_text(update.message.text)
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text("Ok, no problem, come back whenever you want.")
    return ConversationHandler.END


def main():
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("loan", loan)],
            states={
                LoanState.GETCLIENT: [MessageHandler(Filters.text, get_client)]
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    )
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
