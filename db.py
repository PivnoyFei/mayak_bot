import databases
import sqlalchemy
from sqlalchemy import Column, Integer, String, Table, Text
from sqlalchemy.exc import IntegrityError

from settings import DATABASE_URL

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)

parsing = Table(
    "parsing", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(200), unique=True, index=True),
    Column("url", Text),
    Column("xpath", Text),
)
metadata.create_all(engine)


class DataConn:
    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.conn = self.engine.connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class Parsing(DataConn):
    def create(self, name: str, url: str, xpath: str) -> bool:
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
