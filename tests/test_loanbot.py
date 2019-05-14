from bot import loanbot


def test_main_exits_without_error():
    assert not loanbot.main()
