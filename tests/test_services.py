from unittest import mock

from bot import services


@mock.patch("bot.services.db")
@mock.patch("bot.services.requests")
def test_get_client_success(m_requests, m_db, client):
    data = [client]
    response = mock.Mock()
    response.status_code = 200
    response.json.return_value = data
    m_requests.get.return_value = response

    table = mock.Mock()
    table.find_one.return_value = None
    db = {"clients": table}
    m_db.__getitem__.side_effect = db.__getitem__
    m_db.__iter__.side_effect = db.__iter__

    cli = services.get_client("70624771687")

    assert table.find_one.called_once
    assert table.upsert.called_once
    assert m_requests.get.called_once
    assert response.json.called_once
    assert cli == client


@mock.patch("bot.services.db")
@mock.patch("bot.services.requests")
def test_get_client_cached(m_requests, m_db, client):
    table = mock.Mock()
    table.find_one.return_value = client
    db = {"clients": table}
    m_db.__getitem__.side_effect = db.__getitem__
    m_db.__iter__.side_effect = db.__iter__

    cli = services.get_client("70624771687")

    assert table.find_one.called_once
    assert not table.upsert.called
    assert not m_requests.get.called
    assert cli == client


@mock.patch("bot.services.db")
@mock.patch("bot.services.requests")
def test_get_client_not_found(m_requests, m_db):
    response = mock.Mock()
    response.status_code = 200
    response.json.return_value = []
    m_requests.get.return_value = response

    table = mock.Mock()
    table.find_one.return_value = None
    db = {"clients": table}
    m_db.__getitem__.side_effect = db.__getitem__
    m_db.__iter__.side_effect = db.__iter__

    cli = services.get_client("70624771687")

    assert table.find_one.called_once
    assert not table.upsert.called
    assert m_requests.get.called_once
    assert response.json.called_once
    assert not cli


@mock.patch("bot.services.db")
@mock.patch("bot.services.requests")
@mock.patch("bot.loanbot.logger")
def test_get_client_fail(m_logger, m_requests, m_db):
    response = mock.Mock()
    response.status_code = 500
    m_requests.get.return_value = response

    table = mock.Mock()
    table.find_one.return_value = None
    db = {"clients": table}
    m_db.__getitem__.side_effect = db.__getitem__
    m_db.__iter__.side_effect = db.__iter__

    cli = services.get_client("70624771687")

    assert table.find_one.called_once
    assert not table.upsert.called
    assert m_requests.get.called_once
    assert not response.json.called
    assert m_logger.warning.called_once
    assert not cli


@mock.patch("bot.services.db")
@mock.patch("bot.services.requests")
def test_post_loan_success(m_requests, m_db, loan):
    data = {"installment": 85.61}
    response = mock.Mock()
    response.status_code = 201
    response.json.return_value = data
    m_requests.post.return_value = response

    table = mock.Mock()
    db = {"loans": table}
    m_db.__getitem__.side_effect = db.__getitem__
    m_db.__iter__.side_effect = db.__iter__

    installment = services.post_loan(loan)

    data.update(loan)

    assert m_requests.post.called_once
    assert table.upsert.called_once
    assert installment == data


@mock.patch("bot.services.db")
@mock.patch("bot.services.requests")
@mock.patch("bot.loanbot.logger")
def test_post_loan_fail(m_logger, m_requests, m_db, loan):
    response = mock.Mock()
    response.status_code = 400
    m_requests.post.return_value = response

    table = mock.Mock()
    db = {"loans": table}
    m_db.__getitem__.side_effect = db.__getitem__
    m_db.__iter__.side_effect = db.__iter__

    installment = services.post_loan(loan)

    assert m_requests.post.called_once
    assert not table.upsert.called
    assert m_logger.warning.called_once
    assert not installment


@mock.patch("bot.services.db")
def test_get_loan(m_db, client, loan):
    table = mock.Mock()
    table.find_one.return_value = loan
    db = {"loans": table}
    m_db.__getitem__.side_effect = db.__getitem__
    m_db.__iter__.side_effect = db.__iter__

    out = services.get_loan(client.get("client_id", None))

    assert m_db.find_one.called_once
    assert out == loan


@mock.patch("bot.services.requests")
def test_get_balance_success(m_requests, loan):
    data = {"balance": 89.56}
    response = mock.Mock()
    response.status_code = 200
    response.json.return_value = data
    m_requests.get.return_value = response

    out = services.get_balance(loan.get("loan_id", None))

    assert m_requests.get.called_once
    assert out == data


@mock.patch("bot.services.requests")
@mock.patch("bot.loanbot.logger")
def test_get_balance_fail(m_logger, m_requests, loan):
    response = mock.Mock()
    response.status_code = 400
    m_requests.get.return_value = response

    out = services.get_balance(loan.get("loan_id", None))

    assert m_requests.get.called_once
    assert m_logger.warning.called_once
    assert not out


@mock.patch("bot.services.requests")
def test_post_payment_success(m_requests, loan, payment):
    data = payment
    response = mock.Mock()
    response.status_code = 201
    response.json.return_value = data
    m_requests.post.return_value = response

    out = services.post_payment(loan.get("loan_id", None), payment)

    assert m_requests.post.called_once
    assert response.json.called_once
    assert out == data


@mock.patch("bot.services.requests")
def test_post_payment_fail(m_requests, loan, payment):
    response = mock.Mock()
    response.status_code = 400
    m_requests.post.return_value = response

    out = services.post_payment(loan.get("loan_id", None), payment)

    assert m_requests.post.called_once
    assert not response.json.called
    assert not out
