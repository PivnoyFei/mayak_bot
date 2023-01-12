import os
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"

load_dotenv(BASE_DIR / ".env")
TOKEN: Union[str, None] = os.getenv('TOKEN')
DATABASE_URL: Union[str, None] = os.getenv('DATABASE_URL')
