from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy import Column, INTEGER, ForeignKey, String, BOOLEAN, UniqueConstraint, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Movie(Base):
    __tablename__ = "movies"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    release_year = Column(INTEGER, nullable=False)
    watched = Column(BOOLEAN, nullable=False, server_default="false")
    rating = Column(INTEGER)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



# class Vote(Base):
#     __tablename__ = "users"
#     user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
