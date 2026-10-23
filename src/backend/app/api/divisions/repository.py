from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.division_model import Division

async def get_active_divisions(
    db: AsyncSession,
) -> list[Division]:
    result = await db.execute(
        select(Division)
        .where(Division.is_active.is_(True))
        .order_by(Division.name.asc())
    )
    return list(result.scalars().all())