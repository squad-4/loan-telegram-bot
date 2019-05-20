import json
import logging
import re
from datetime import datetime
from enum import Enum, auto

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from bot import services, settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.LOG_LEVEL),
)
logger = logging.getLogger(__name__)


class LoanState(Enum):
    GETCLIENT = auto()
    NEWLOAN = auto()
    CREATELOAN = auto()


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


def whom(update, context):
    update.message.reply_text("Please, send me your CPF number.")
    return LoanState.GETCLIENT


def get_client(update, context):
    cpf = re.sub("[^0-9]", "", update.message.text)
    client = services.get_client(cpf)

    if client:
        context.user_data["client"] = client
        text = json.dumps(client, indent=2)
        update.message.reply_markdown(f"```json\n{text}\n```")
        update.message.reply_text(
            "This is what I got. Is this the right client?",
            reply_markup=ReplyKeyboardMarkup(
                [["Yes", "No"]], one_time_keyboard=True
            ),
        )
        return LoanState.NEWLOAN
    else:
        update.message.reply_text("Sorry, I couldn't find the client.")
        return ConversationHandler.END


def new_loan(update, context):
    answer = update.message.text

    if answer == "Yes":
        update.message.reply_text(
            (
                "I need the loan amount and the payment term. "
                "You can also opt for an interest rate, "
                "by default we apply 5% yr.\n\n"
                "e.g. $5000.00 in 12 mo"
            ),
            reply_markup=ReplyKeyboardRemove(),
        )
        return LoanState.CREATELOAN

    update.message.reply_text(
        "Ok then, please send me another CPF number.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return LoanState.GETCLIENT


def create_loan(update, context):
    values = re.findall(r"\d+\.?\d*", update.message.text)
    n_values = len(values)

    if 2 <= n_values <= 3:
        loan = {
            "amount": float(values[0]),
            "term": int(values[1]),
            "rate": float(values[2]) if n_values == 3 else 0.05,
            "date": datetime.now().isoformat(timespec="seconds"),
            "client_id": context.user_data["client"]["client_id"],
        }
        context.user_data["loan"] = loan
        deal = services.post_loan(loan)
        text = "Sorry, but this client has a pending loan."

        if deal:
            text = (
                f"Done! Here's the deal: ${loan['amount']:.02f} paid in "
                f"{loan['term']} installments of ${deal['installment']:.02f}."
            )

        update.message.reply_text(text)
        return ConversationHandler.END

    update.message.reply_text(
        (
            "I can't apply for a loan without an amount and term. "
            "Let's try it again, send me a loan amount and the payment term."
        )
    )
    return LoanState.CREATELOAN


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
            entry_points=[CommandHandler("loan", whom)],
            states={
                LoanState.GETCLIENT: [
                    MessageHandler(
                        Filters.text, get_client, pass_user_data=True
                    )
                ],
                LoanState.NEWLOAN: [
                    MessageHandler(Filters.text, new_loan, pass_user_data=True)
                ],
                LoanState.CREATELOAN: [
                    MessageHandler(
                        Filters.text, create_loan, pass_user_data=True
                    )
                ],
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
