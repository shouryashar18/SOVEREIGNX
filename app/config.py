import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://127.0.0.1:27017"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "sih_workbench"
)