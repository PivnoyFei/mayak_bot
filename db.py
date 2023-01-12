from typing import Any

import sqlalchemy
from sqlalchemy import Column, Integer, String, Table, Text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError

from settings import DATABASE_URL

metadata = sqlalchemy.MetaData()
engine: Engine = sqlalchemy.create_engine(DATABASE_URL)

parsing = Table(
    "parsing", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(200), unique=True, index=True),
    Column("url", Text),
    Column("xpath", Text),
)
metadata.create_all(engine)


class DataConn:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def __enter__(self) -> Any:
        self.conn = self.engine.connect()
        return self.conn

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.conn.close()


class Parsing(DataConn):
    async def create(self, name: str, url: str, xpath: str) -> bool:
        try:
            with DataConn(engine) as conn:
                query = (
                    parsing.insert()
                    .values(name=name, url=url, xpath=xpath)
                )
                conn.execute(query)
            return True
        except IntegrityError:
            return False
