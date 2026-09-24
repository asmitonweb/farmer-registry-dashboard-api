import sys

code = '''from fastapi import APIRouter, Depends, Query
import asyncpg
from typing import List, Dict, Any, Optional
from app.api.dependencies import get_db_pool

router = APIRouter()

def build_where_clause(region, zone, woreda, kebele, farmingType):
    conditions = []
    values = []
    idx = 1
    if region and region != 'all':
        # Assuming geo_1 is region_code
        conditions.append(f"geo_1 = ")
        values.append(region)
        idx += 1
    if zone and zone != 'all':
        conditions.append(f"geo_2 = ")
        values.append(zone)
        idx += 1
    if woreda and woreda != 'all':
        conditions.append(f"geo_3 = ")
        values.append(woreda)
        idx += 1
    if kebele and kebele != 'all':
        conditions.append(f"geo_4 = ")
        values.append(kebele)
        idx += 1
    if farmingType and farmingType != 'all':
        conditions.append(f"main_farming_type = ")
        values.append(farmingType)
        idx += 1
    
    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)
    return where, values

@router.get("/farmersByRegion", response_model=List[Dict[str, Any]])
async def get_farmers_by_region(
    region: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    woreda: Optional[str] = Query(None),
    kebele: Optional[str] = Query(None),
    farmingType: Optional[str] = Query(None),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    where, values = build_where_clause(region, zone, woreda, kebele, farmingType)
    query = f"""
        SELECT
            COALESCE(geo_1, 'Unknown') as region,
            COALESCE(geo_1, 'Unknown') as region_code,
            COUNT(DISTINCT farmer_id) as farmers
        FROM fr_rpt_farmer
        {where}
        GROUP BY 1, 2
        ORDER BY farmers DESC
    """
    async with pool.acquire() as conn:
        records = await conn.fetch(query, *values)
    return [dict(r) for r in records]

@router.get("/farmersByGender", response_model=List[Dict[str, Any]])
async def get_farmers_by_gender(
    region: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    woreda: Optional[str] = Query(None),
    kebele: Optional[str] = Query(None),
    farmingType: Optional[str] = Query(None),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    where, values = build_where_clause(region, zone, woreda, kebele, farmingType)
    query = f"""
        SELECT
            COALESCE(gender, 'Unknown') as gender,
            COUNT(DISTINCT farmer_id) as farmers
        FROM fr_rpt_farmer
        {where}
        GROUP BY 1
        ORDER BY farmers DESC
    """
    async with pool.acquire() as conn:
        records = await conn.fetch(query, *values)
    return [dict(r) for r in records]

@router.get("/farmersByType", response_model=List[Dict[str, Any]])
async def get_farmers_by_type(
    region: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    woreda: Optional[str] = Query(None),
    kebele: Optional[str] = Query(None),
    farmingType: Optional[str] = Query(None),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    where, values = build_where_clause(region, zone, woreda, kebele, farmingType)
    query = f"""
        SELECT
            COALESCE(main_farming_type, 'Unknown') as farming_type,
            COUNT(DISTINCT farmer_id) as farmers
        FROM fr_rpt_farmer
        {where}
        GROUP BY 1
        ORDER BY farmers DESC
    """
    async with pool.acquire() as conn:
        records = await conn.fetch(query, *values)
    return [dict(r) for r in records]
'''
with open('app/api/routes/charts.py', 'w') as f:
    f.write(code)
