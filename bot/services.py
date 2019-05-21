import logging
from datetime import datetime

import dataset
import requests

from bot import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.LOG_LEVEL),
)
logger = logging.getLogger(__name__)

engine_config = (
    {"connect_args": {"check_same_thread": False}}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)
db = dataset.connect(settings.DATABASE_URL, engine_kwargs=engine_config)


def get_client(cpf):
    table = db["clients"]
    cpf = cpf if cpf else "00000000000"
    client = table.find_one(cpf=cpf) or {}

    if client:
        return client

    url = f"{settings.LOAN_API}/clients/?cpf={cpf}"
    response = requests.get(url)

    if response.status_code == 200:
        client = response.json()

        if not client:
            return

        client = client[0]
        id = client.pop("id", None)
        client["client_id"] = id
        table.upsert(client, ["cpf"])
        return client

    logger.warning("Error retrieving client with CPF %s", cpf)


def post_loan(data):
    url = f"{settings.LOAN_API}/loans/"
    response = requests.post(url, json=data)

    if response.status_code == 201:
        loan = data
        loan.update(response.json())
        table = db["loans"]
        table.upsert(loan, ["client_id"])
        return loan

    logger.warning(
        "Error creating a new loan for client %s", data.get("client_id", None)
    )


def get_loan(client_id):
    table = db["loans"]
    return table.find_one(client_id=client_id) or {}


def get_balance(loan_id):
    date = datetime.now().isoformat(timespec="seconds")
    url = f"{settings.LOAN_API}/loans/{loan_id}/balance/?date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    logger.warning("Error retrieving balance for loan %s", loan_id)
