from decouple import config

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", default="")
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOAN_API = config("LOAN_API", default="http://localhost")
DATABASE_URL = config("DATABASE_URL", default="sqlite:///:memory:")
