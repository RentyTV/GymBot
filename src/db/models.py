from sqlalchemy import DateTime, func, BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    username: Mapped[str]
    g_days: Mapped[int]
    g_sets: Mapped[int]
    g_timer: Mapped[float] 
    g_status: Mapped[bool]


class User_Training(Base):
    __tablename__ = 'users_training'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    arme: Mapped[bool] = mapped_column(default=False)
    rucken: Mapped[bool] = mapped_column(default=False)
    bauch: Mapped[bool] = mapped_column(default=False)
    beine: Mapped[bool] = mapped_column(default=False)
    brust: Mapped[bool] = mapped_column(default=False)
    arme_sets: Mapped[int] = mapped_column(default=0)
    rucken_sets: Mapped[int] = mapped_column(default=0)
    bauch_sets: Mapped[int] = mapped_column(default=0)
    beine_sets: Mapped[int] = mapped_column(default=0)
    brust_sets: Mapped[int] = mapped_column(default=0)


class User_Sets(Base):
    __tablename__ = 'users_sets'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    set_id: Mapped[str]
    user_id: Mapped[int] = mapped_column(BigInteger)
    muskul_typ: Mapped[str]
    notiz: Mapped[str]
    repetitions: Mapped[int] = mapped_column(default=0)