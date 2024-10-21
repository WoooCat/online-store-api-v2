from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def transaction_context(db: AsyncSession):
    try:
        yield db
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
