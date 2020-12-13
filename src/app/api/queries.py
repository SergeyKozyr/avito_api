from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from app.api import crud
from app.api.models import SearchQuery, Counter


router = APIRouter()


@router.get('/stat/{query_id}', response_model=List[Counter])
async def get_query(query_id: int,
                    interval_start: datetime = '2020-11-20 12:59:11',
                    interval_end: datetime = '2020-11-20 16:59:11'):

    start_datetime = datetime.strptime(interval_start, '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(interval_end, '%Y-%m-%d %H:%M:%S')
    query = await crud.get(query_id, start_datetime, end_datetime)
    if not query:
        raise HTTPException(status_code=404, detail='SearchQuery not found')
    return query


@router.post('/add', status_code=201)
async def create_query(payload: SearchQuery) -> dict:
    query_id = await crud.post(payload)
    await crud.create_counter(query_id)
    return {'id': query_id}


@router.delete('/{query_id}/')
async def delete_query(query_id: int) -> dict:
    await crud.delete_counters(query_id)
    await crud.delete_query(query_id)
    return {'Deleted search query with id': query_id}


@router.get('/top5_deals/{query_id}')
async def get_top5_deals(query_id: int) -> List[str]:
    query = await crud.get_top5_deals_by_id(query_id)
    if not query:
        raise HTTPException(status_code=404, detail='SearchQuery not found')
    return query
