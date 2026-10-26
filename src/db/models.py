from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config import IST


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    topics: Mapped[list["Topics"]] = relationship("Topics", back_populates="created_by_user")
    work_updates: Mapped[list["WorkUpdates"]] = relationship("WorkUpdates", back_populates="user")


class Topics(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_by_user: Mapped[Users] = relationship(Users, back_populates="topics")
    work_updates: Mapped[list["WorkUpdates"]] = relationship("WorkUpdates", back_populates="topic")


class WorkUpdates(Base):
    __tablename__ = "work_updates"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey('topics.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user: Mapped[Users] = relationship(Users, back_populates="work_updates")
    topic: Mapped[Topics] = relationship("Topics", back_populates="work_updates")

    def to_dict(self):
        ist_timestamp = self.created_at.astimezone(tz=IST)
        return {
            "id": self.id,
            "topic": self.topic.topic_name,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_name": f"{self.user.first_name} {self.user.last_name}",
            "date_of_creation": ist_timestamp.date(),
            "time_of_creation": ist_timestamp.time().strftime("%I:%M %p"),
        }
