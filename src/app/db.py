import os

from sqlalchemy import (Column, Integer, MetaData, String, Table, DateTime,
                        create_engine)
from sqlalchemy.sql import func
from databases import Database

TESTING = os.getenv('TESTING')

if TESTING:
    DATABASE_URL = os.getenv('TEST_DATABASE_URL')
    database = Database(DATABASE_URL, force_rollback=True)
else:
    DATABASE_URL = os.getenv('DATABASE_URL')
    database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
metadata = MetaData()

queries = Table(
    'queries',
    metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('text', String(50)),
    Column('region', String(30)),
)

counters = Table(
    'counters',
    metadata,
    Column('query_id', Integer),
    Column('number_of_deals', Integer),
    Column('timestamp', DateTime(timezone=True), server_default=func.now())
)
