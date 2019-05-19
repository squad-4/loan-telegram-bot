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
        ("loan", loanbot.LoanState.GETCLIENT),
        ("get_client", loanbot.ConversationHandler.END),
        ("cancel", loanbot.ConversationHandler.END),
    ],
)
def test_command(cmd, exp, update, context):
    command = getattr(loanbot, cmd)
    out = command(update, context)
    assert update.message.reply_text.called_once
    assert out == exp


@mock.patch("bot.loanbot.logger")
def test_error(m_logger, update, context):
    loanbot.error(update, context)
    assert m_logger.warning.called_once
    assert update.called_once
    assert context.error.called_once
