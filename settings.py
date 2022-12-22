import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"

load_dotenv(BASE_DIR / ".env")
TOKEN: str = os.getenv('TOKEN')
DATABASE_URL: str = os.getenv('DATABASE_URL')
