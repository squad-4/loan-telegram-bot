from unittest import mock

from bot import services


@mock.patch("bot.services.requests")
def test_get_client_success(m_requests, client):
    data = [client]
    response = mock.Mock()
    response.status_code = 200
    response.json.return_value = data
    m_requests.get.return_value = response
    client = services.get_client("70624771687")
    assert m_requests.get.called_once
    assert client == data[0]


@mock.patch("bot.services.requests")
@mock.patch("bot.loanbot.logger")
def test_get_client_fail(m_logger, m_requests):
    response = mock.Mock()
    response.status_code = 500
    m_requests.get.return_value = response
    client = services.get_client("70624771687")
    assert m_requests.get.called_once
    assert m_logger.warning.called_once
    assert not client
