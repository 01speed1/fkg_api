from app.db.connections import postgres as db
from app.schemas.support_case import SupportCase, SupportCaseInDB, SupportCaseStatus

TABLE = "support_cases"

class SupportCaseModel:
  async def create(self, support_case: SupportCase) -> SupportCaseInDB:
    created_case = await db.insert(TABLE, support_case.model_dump())

    return SupportCaseInDB(**created_case)

  async def get_all(self, limit: int = 10, offset: int = 0) -> list[SupportCaseInDB]:
    query = f"SELECT * FROM {TABLE} LIMIT %s OFFSET %s"
    values = (limit, offset,)
    rows = await db.fetch(query, values)
    
    if not rows:
        return []

    return [SupportCaseInDB(**row) for row in rows]
  
  async def get_by_id(self, case_id: int) -> SupportCaseInDB:
    query = f"SELECT * FROM {TABLE} WHERE id = %s"
    values = (case_id,)
    row = await db.fetch_one(query, values)

    if not row:
        return None

    return SupportCaseInDB(**row)
  
  
  async def update_one(self, case_id: int, status: SupportCaseStatus) -> SupportCaseInDB:

    query = f"UPDATE {TABLE} SET status = %s WHERE id = %s RETURNING *"
    values = (status, case_id,)
    updated_row = await db.execute(query, values)

    if not updated_row:
        return None

    return SupportCaseInDB(**updated_row[0])