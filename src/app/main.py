from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from app.db import queries, database, metadata, engine
from app.api import queries as queries_api, crud


metadata.create_all(engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('startup')
@repeat_every(seconds=3600, wait_first=True)
async def get_new_counters():
    db_query = queries.select()
    all_records = await database.fetch_all(query=db_query)
    for record in all_records:
        await crud.create_counter(record['id'])


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(queries_api.router)
