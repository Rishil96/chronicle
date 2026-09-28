from datetime import datetime, date, time
from zoneinfo import ZoneInfo
from sqlalchemy import String, Date, Time, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# IST Timezone
IST = ZoneInfo("Asia/Kolkata")


class Base(DeclarativeBase):
    pass


class Logs(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    entry: Mapped[str] = mapped_column(String(1000))
    date_of_creation: Mapped[date] = mapped_column(Date, default=lambda: datetime.now(tz=IST).date())
    time_of_creation: Mapped[time] = mapped_column(Time, default=lambda: datetime.now(tz=IST).time())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=IST))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "entry": self.entry,
            "date_of_creation": self.date_of_creation,
            "time_of_creation": self.time_of_creation.strftime("%I:%M %p"),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=IST))


class WorkCategories(Base):
    __tablename__ = "work_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=IST))


class Projects(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_name: Mapped[str] = mapped_column(String(100), unique=True)
    client_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=IST))


class DailyUpdates(Base):
    __tablename__ = "daily_updates"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    short_description: Mapped[str] = mapped_column(String(250), nullable=False)
    long_description: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=IST))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
