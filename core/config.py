import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5433))  # ← MUST BE 5433
DB_NAME = os.getenv("DB_NAME", "workflowos")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Mohsin557788@")

POSTGRES_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}

PLUGINS_PATH = "plugins"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")