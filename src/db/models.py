from datetime import datetime, date, time
from sqlalchemy import String, Date, Time, DateTime, Boolean, Text, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from src.config import IST


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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    work_updates: Mapped[list["WorkUpdates"]] = relationship("DailyUpdates", back_populates="user")


class Topics(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WorkUpdates(Base):
    __tablename__ = "work_updates"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey('topics.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=IST))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user: Mapped[Users] = relationship(Users, back_populates="work_updates")
    topic: Mapped[Topics] = relationship("Topics", back_populates="work_updates")

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic.topic_name,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_name": f"{self.user.first_name} {self.user.last_name}",
            "date_of_creation": self.created_at.date(),
            "time_of_creation": self.updated_at.time().strftime("%I:%M %p") if self.updated_at else self.created_at.time().strftime("%I:%M %p"),
        }
