from sqlalchemy import Integer, String, ForeignKey, Column, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(127), nullable=False, unique=True)

    user_profile = relationship("Profile", back_populates="user")
    user_post = relationship("Post", back_populates="user")
    user_article = relationship("Article", back_populates="user")


class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=True)
    fullname = Column(String(127), nullable=True)
    user_idx = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="user_profile")


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(31), nullable=False)
    content = Column(String)
    user_idx = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="user_post")


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    template = Column(String(127), nullable=False)
    user_idx = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="user_article")
