from unittest import mock

from bot import loanbot


@mock.patch("bot.loanbot.Updater")
@mock.patch("bot.loanbot.CommandHandler")
def test_main_exits_without_error(m_CommandHandler, m_Updater):
    assert not loanbot.main()


def test_start(update, context):
    loanbot.start(update, context)
    assert context.bot.send_message.called_once
    assert update.message.chat_id.called_once


def test_help(update, context):
    loanbot.help(update, context)
    assert context.bot.send_message.called_once
    assert update.message.chat_id.called_once


@mock.patch("bot.loanbot.logger")
def test_error(m_logger, update, context):
    loanbot.error(update, context)
    assert m_logger.warning.called_once
    assert update.called_once
    assert context.error.called_once
