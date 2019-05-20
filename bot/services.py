import logging

import requests

from bot import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.LOG_LEVEL),
)
logger = logging.getLogger(__name__)


def get_client(cpf):
    url = f"{settings.LOAN_API}/clients/?cpf={cpf}"
    response = requests.get(url)

    if response.status_code == 200:
        client = response.json()
        return client[0] if client else None

    logger.warning("Error retrieving client with CPF %s", cpf)


def post_loan(data):
    url = f"{settings.LOAN_API}/loans/"
    response = requests.post(url, json=data)

    if response.status_code == 201:
        return response.json()

    logger.warning(
        "Error creating a new loan for client %s", data.get("client_id", None)
    )
