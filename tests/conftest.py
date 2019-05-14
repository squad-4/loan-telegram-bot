from unittest import mock

import pytest


@pytest.fixture
def update():
    up = mock.Mock()
    up.message.chat_id.return_value = 1
    return up


@pytest.fixture
def context():
    ct = mock.Mock()
    ct.error.return_value = "SEGFAULT"
    return ct
