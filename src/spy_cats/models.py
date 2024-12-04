from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint, Integer, Boolean, ForeignKey

from src.database import Base


class SpyCat(Base):
    __tablename__ = "spy_cat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    years_experience: Mapped[int] = mapped_column(Integer, CheckConstraint('years_experience >= 0 AND years_experience <= 50'))
    breed: Mapped[str] = mapped_column(String(4))
    salary: Mapped[int] = mapped_column(Integer, CheckConstraint('salary > 0'))
    mission: Mapped[Optional["Mission"]] = relationship(back_populates="spy_cat")


class Mission(Base):
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    spy_cat_id: Mapped[Optional[int]] = mapped_column(ForeignKey("spy_cat.id"), nullable=True)
    spy_cat: Mapped[Optional["SpyCat"]] = relationship(back_populates="mission", single_parent=True)
    targets: Mapped[List["Target"]] = relationship()


class Target(Base):
    __tablename__ = "target"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    notes: Mapped[List["TargetNote"]] = relationship()


class TargetNote(Base):
    __tablename__ = "target_note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(1000))
    target_id: Mapped[int] = mapped_column(ForeignKey("target.id"))
