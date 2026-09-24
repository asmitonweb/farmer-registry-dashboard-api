from fastapi import APIRouter, Depends
import asyncpg
from typing import List, Dict, Any
from app.api.dependencies import get_db_pool

router = APIRouter()

@router.get("/farmersByRegion", response_model=List[Dict[str, Any]])
async def get_farmers_by_region(pool: asyncpg.Pool = Depends(get_db_pool)):
    query = """
        SELECT
            COALESCE(geo_1, 'Unknown') as region,
            COALESCE(geo_1, 'Unknown') as region_code,
            COUNT(DISTINCT internal_record_id) as farmers
        FROM fr_rpt_farmer
        GROUP BY 1, 2
        ORDER BY farmers DESC
    """
    async with pool.acquire() as conn:
        records = await conn.fetch(query)
    return [dict(r) for r in records]

@router.get("/farmersByGender", response_model=List[Dict[str, Any]])
async def get_farmers_by_gender(pool: asyncpg.Pool = Depends(get_db_pool)):
    query = """
        SELECT
            COALESCE(gender, 'Unknown') as gender,
            COUNT(DISTINCT internal_record_id) as farmers
        FROM fr_rpt_farmer
        GROUP BY 1
        ORDER BY farmers DESC
    """
    async with pool.acquire() as conn:
        records = await conn.fetch(query)
    return [dict(r) for r in records]

@router.get("/farmersByType", response_model=List[Dict[str, Any]])
async def get_farmers_by_type(pool: asyncpg.Pool = Depends(get_db_pool)):
    query = """
        SELECT
            COALESCE(main_farming_type, 'Unknown') as farming_type,
            COUNT(DISTINCT internal_record_id) as farmers
        FROM fr_rpt_farmer
        GROUP BY 1
        ORDER BY farmers DESC
    """
    async with pool.acquire() as conn:
        records = await conn.fetch(query)
    return [dict(r) for r in records]
