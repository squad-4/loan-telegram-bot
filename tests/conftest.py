from unittest import mock

import pytest


@pytest.fixture
def update():
    up = mock.Mock()
    up.message.text = "A message"
    return up


@pytest.fixture
def context():
    ct = mock.Mock()
    ct.error = "SEGFAULT"
    ct.user_data = {}
    return ct


@pytest.fixture
def client():
    return {
        "client_id": "1e4c777d-ec05-4b0b-b4be-10cb5a0d1e82",
        "name": "Herman",
        "surname": "Melville",
        "email": "whale@pequod.ship",
        "telephone": "+442072343456",
        "date": "2019-05-18T23:52:15.753070Z",
        "cpf": "70624771687",
    }


@pytest.fixture
def loan():
    return {
        "loan_id": "5a8e9343-3535-4981-b766-4e6a229ccb50",
        "amount": 1000.0,
        "term": 12,
        "rate": 0.05,
        "date": "2019-05-19T20:00:00",
        "client_id": "1e4c777d-ec05-4b0b-b4be-10cb5a0d1e82",
    }
