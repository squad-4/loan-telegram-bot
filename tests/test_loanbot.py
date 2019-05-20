from unittest import mock

from pytest import mark

from bot import loanbot


@mock.patch("bot.loanbot.Updater")
@mock.patch("bot.loanbot.MessageHandler")
@mock.patch("bot.loanbot.Filters")
@mock.patch("bot.loanbot.ConversationHandler")
@mock.patch("bot.loanbot.CommandHandler")
def test_main_exits_without_error(
    m_CommandHandler,
    m_ConversationHandler,
    m_Filters,
    m_MessageHandler,
    m_Updater,
):
    assert not loanbot.main()


@mark.parametrize(
    "cmd,exp",
    [
        ("start", None),
        ("help", None),
        ("unknown", None),
        ("whom", loanbot.LoanState.GETCLIENT),
        ("cancel", loanbot.ConversationHandler.END),
    ],
)
def test_command(cmd, exp, update, context):
    command = getattr(loanbot, cmd)
    out = command(update, context)
    assert update.message.reply_text.called_once
    assert out == exp


@mock.patch("bot.loanbot.ReplyKeyboardMarkup")
@mock.patch("bot.loanbot.services")
def test_get_client_found(
    m_services, m_ReplyKeyboardMarkup, update, context, client
):
    m_services.get_client.return_value = client
    out = loanbot.get_client(update, context)
    assert update.message.reply_markdown.called_once
    assert update.message.reply_text.called_once
    assert m_ReplyKeyboardMarkup.called_once
    assert out == loanbot.LoanState.NEWLOAN


@mock.patch("bot.loanbot.ReplyKeyboardMarkup")
@mock.patch("bot.loanbot.services")
def test_get_client_not_found(
    m_services, m_ReplyKeyboardMarkup, update, context
):
    m_services.get_client.return_value = None
    out = loanbot.get_client(update, context)
    assert not update.message.reply_markdown.called
    assert update.message.reply_text.called_once
    assert not m_ReplyKeyboardMarkup.called
    assert out == loanbot.ConversationHandler.END


@mock.patch("bot.loanbot.ReplyKeyboardRemove")
def test_new_loan_yes(m_ReplyKeyboardRemove, update, context):
    update.message.text = "Yes"
    out = loanbot.new_loan(update, context)
    assert update.message.reply_text.called_once
    assert m_ReplyKeyboardRemove.called_once
    assert out == loanbot.LoanState.CREATELOAN


@mock.patch("bot.loanbot.ReplyKeyboardRemove")
def test_new_loan_no(m_ReplyKeyboardRemove, update, context):
    update.message.text = "No"
    out = loanbot.new_loan(update, context)
    assert update.message.reply_text.called_once
    assert m_ReplyKeyboardRemove.called_once
    assert out == loanbot.LoanState.GETCLIENT


@mock.patch("bot.loanbot.services")
def test_create_loan_no_values(m_services, update, context):
    out = loanbot.create_loan(update, context)
    assert not m_services.post_loan.called
    assert update.message.reply_text.called_once
    assert out == loanbot.LoanState.CREATELOAN


@mock.patch("bot.loanbot.services")
def test_create_loan_success(m_services, update, context):
    update.message.text = "1000.00 12"
    context.user_data["client"] = {"client_id": "userid"}
    m_services.post_loan.return_value = {"installment": 85.61}
    out = loanbot.create_loan(update, context)
    assert m_services.post_loan.called_once
    assert update.message.reply_text.called_once
    assert out == loanbot.ConversationHandler.END


@mock.patch("bot.loanbot.logger")
def test_error(m_logger, update, context):
    loanbot.error(update, context)
    assert m_logger.warning.called_once
    assert update.called_once
    assert context.called_once
