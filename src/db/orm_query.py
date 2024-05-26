from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import *
from sqlalchemy import DateTime
from datetime import datetime, date


async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    username: str | None = None,
    g_days: int | None = None,
    g_sets: int| None = None,
    g_timer: float| None = None,
    g_status: int| None = None,
):
    query = select(Users).where(Users.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            Users(user_id=user_id, username=username, g_days=g_days, g_sets=g_sets, g_timer=g_timer, g_status=g_status)
        )
        await session.commit()


async def orm_get_total_users(session: AsyncSession):
    query = select(Users)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(Users).where(Users.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_user(session: AsyncSession, user_id: int, **values):
    query = update(Users).where(Users.user_id == user_id).values(**values)
    await session.execute(query)
    await session.commit()


async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(Users).where(Users.id == user_id)
    await session.execute(query)
    await session.commit()


# User trainings erstellen
async def orm_add_user_training(session: AsyncSession, user_id: int):
    user_training = User_Training(user_id=user_id)
    session.add(user_training)
    await session.commit()


async def orm_get_user_training_via_data(session: AsyncSession, user_id: int, created_date: date):
    query = select(User_Training).where(User_Training.user_id == user_id).where(func.date(User_Training.created) == created_date)
    # query = select(User_Training).where(func.substr(User_Training.created, 0, 9) == created_date)
    # query = select(User_Training).where(User_Training.created, 0, 9 == created_date)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_user_training(session: AsyncSession, created_date: DateTime, **values):
    query = update(User_Training).where(User_Training.created, 1, 10 == created_date).values(**values)
    await session.execute(query)
    await session.commit()


# Alles mit sets
async def orm_add_user_sets(session: AsyncSession, set_id: int, user_id: int, muskul_typ: str | None,  user_notiz: str | None, repetitions: int | None):
    user_set = User_Sets(set_id=set_id, user_id=user_id, muskul_typ=muskul_typ, notiz=user_notiz, repetitions=repetitions)
    session.add(user_set)
    await session.commit()


async def orm_check_user_sets(session: AsyncSession, set_id: str):
    query = select(User_Sets).where(User_Sets.set_id == set_id)
    result = await session.execute(query)
    if result.scalar():
        return True
    else:
        return False


async def orm_get_user_set(session: AsyncSession, set_id: str):
    query = select(User_Sets).where(User_Sets.set_id == set_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_user_sets(session: AsyncSession, set_id: str, **values):
    query = update(User_Sets).where(User_Sets.set_id == set_id).values(**values)
    await session.execute(query)
    await session.commit()


async def orm_get_all_user_sets(session: AsyncSession, user_id: int):
    query = select(User_Sets).where(getattr(User_Sets, user_id) == user_id)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


async def orm_delete_all_user_sets(session: AsyncSession, user_id: int):
    query = delete(User_Sets).where(getattr(User_Sets, user_id) == user_id)
    await session.execute(query)
    await session.commit()
