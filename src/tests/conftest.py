import os
import pytest

from app.db import database, metadata, engine

os.environ['TESTING'] = 'True'


@pytest.fixture(scope='function')
async def test_db():
    metadata.create_all(engine)
    await database.connect()
    yield database
    metadata.drop_all(engine)
    await database.disconnect()
