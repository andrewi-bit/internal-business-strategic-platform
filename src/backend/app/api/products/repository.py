from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_model import Product
from app.models.product_status_model import ProductStatus

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, product_status_id: UUID | None = None):
        query = select(Product, ProductStatus).join(
            ProductStatus,
            ProductStatus.id == Product.product_status_id,
        )

        if product_status_id is not None:
            query = query.where(Product.product_status_id == product_status_id)

        result = await self.db.execute(query.order_by(Product.product_name.asc()))
        return result.all()

    async def get_by_id(self, product_id: UUID):
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, product_name: str):
        result = await self.db.execute(
            select(Product).where(
                func.lower(Product.product_name) == product_name.lower()
            )
        )
        return result.scalar_one_or_none()

    async def get_status_by_id(self, product_status_id: UUID):
        result = await self.db.execute(
            select(ProductStatus).where(ProductStatus.id == product_status_id)
        )
        return result.scalar_one_or_none()

    async def create(self, product: Product):
        self.db.add(product)
        await self.db.flush()
        return product

    async def try_delete(self, product: Product) -> bool:
        # False jika database menolak karena product masih dipakai project.
        try:
            async with self.db.begin_nested():
                await self.db.delete(product)
                await self.db.flush()
        except IntegrityError:
            return False

        return True

    async def save(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
