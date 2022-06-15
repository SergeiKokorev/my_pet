from sqlalchemy import Integer, String, ForeignKey, Column, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import text

from .database import Base


class BaseUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(127), nullable=False, unique=True)
    password = Column(String(127), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=text('now()'))

    user_profile = relationship("UserProfile", back_populates="user")
    user_post = relationship("Post", back_populates="user")
    user_article = relationship("Article", back_populates="user")


class UserProfile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    first_name = Column(String(31), nullable=True)
    last_name = Column(String(127), nullable=True)
    user_idx = Column(Integer, ForeignKey("users.id"), 
                      nullable=False, unique=True)

    user = relationship("BaseUser", back_populates="user_profile")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(31), nullable=False)
    content = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_idx = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("BaseUser", back_populates="user_post")


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    template = Column(String(127), nullable=False)
    user_idx = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    user = relationship("BaseUser", back_populates="user_article")
