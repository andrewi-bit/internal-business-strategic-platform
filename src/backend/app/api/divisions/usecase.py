from sqlalchemy.ext.asyncio import AsyncSession

from app.api.divisions import repository
from app.api.divisions.schema import DivisionResponse

async def list_active_divisions(
    db: AsyncSession,
) -> list[DivisionResponse]:
    divisions = await repository.get_active_divisions(db)

    return [
        DivisionResponse.model_validate(division)
        for division in divisions
    ]