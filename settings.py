import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"

DATABASE_URL = "sqlite:///sqlite3.db"

load_dotenv(BASE_DIR / ".env")
TOKEN: str = os.getenv('TOKEN')
