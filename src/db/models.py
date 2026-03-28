from datetime import datetime, date, time
from sqlalchemy import String, Date, Time, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Logs(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    entry: Mapped[str] = mapped_column(String(1000))
    date_of_creation: Mapped[date] = mapped_column(Date)
    time_of_creation: Mapped[time] = mapped_column(Time)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
