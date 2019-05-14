from decouple import config

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", default="")
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
