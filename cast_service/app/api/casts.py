#~/python-microservices/cast-service/app/api/casts.py

from fastapi import APIRouter, HTTPException
from typing import List

from app.api.models import CastOut, CastIn, CastUpdate
from app.api import db_manager

casts = APIRouter()

@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await db_manager.add_cast(payload)

    response = {
        'id': cast_id,
        **payload.dict()
    }

    return response

@casts.get('/{id}/', response_model=CastOut)
async def get_cast(id: int):
    cast = await db_manager.get_cast(id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast

@casts.get('/', response_model=List[CastOut])
async def get_casts():
    return await db_manager.get_all_casts()

@casts.delete('/{id}', response_model=None)
async def delete_cast(id: int):
    cast = await db_manager.get_cast(id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return await db_manager.delete_cast(id)

@casts.put('/{id}/', response_model = CastOut)
async def update_cast(id: int, payload: CastUpdate):
    cast = await db_manager.get_cast(id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    update_data = payload.dict(exclude_unset=True)

    cast_in_db = CastIn(**cast)
    updated_cast = cast_in_db.copy(update=update_data)
    return await db_manager.update_cast(id, updated_cast)