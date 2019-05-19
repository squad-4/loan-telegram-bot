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
        "id": "1e4c777d-ec05-4b0b-b4be-10cb5a0d1e82",
        "name": "Herman",
        "surname": "Melville",
        "email": "whale@pequod.ship",
        "telephone": "+442072343456",
        "date": "2019-05-18T23:52:15.753070Z",
        "cpf": "70624771687",
    }
