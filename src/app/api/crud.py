from datetime import datetime
from sqlalchemy import and_
from app.api.models import SearchQuery
from app.db import queries, counters, database
from .avito_tools import get_number_of_deals, get_top5_deals


async def post(payload: SearchQuery):
    db_query = queries.insert().values(
        text=payload.text,
        region=payload.region
    )
    return await database.execute(query=db_query)


async def get(query_id: int, interval_start: datetime, interval_end: datetime):
    db_query = counters.select().where(
        and_(
            query_id == queries.c.id,
            interval_end >= counters.c.timestamp,
            interval_start <= counters.c.timestamp
        )
    )
    return await database.fetch_all(query=db_query)


async def delete_query(query_id: int):
    db_query = queries.delete().where(query_id == queries.c.id)
    return await database.execute(query=db_query)


async def delete_counters(query_id: int):
    db_query = counters.delete().where(query_id == counters.c.query_id)
    return await database.execute(query=db_query)


async def create_counter(query_id: int):
    db_query = queries.select().where(query_id == queries.c.id)
    selected_query = await database.fetch_one(query=db_query)

    number_of_deals = get_number_of_deals(
        selected_query['text'],
        selected_query['region']
    )

    db_query = counters.insert().values(
        query_id=query_id,
        number_of_deals=number_of_deals
    )
    await database.execute(query=db_query)


async def get_top5_deals_by_id(query_id: int):
    db_query = queries.select().where(query_id == queries.c.id)
    selected_query = await database.fetch_one(query=db_query)
    top5_deals = get_top5_deals(
        selected_query['text'],
        selected_query['region']
    )
    return top5_deals
