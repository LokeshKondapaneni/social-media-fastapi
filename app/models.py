from sqlalchemy.sql import expression
from sqlalchemy.orm import Relationship
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from .database import Base

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    #published = Column(Boolean, default=True) # This sets the value to default on sqlalchemy level and when you insert or like it gets added
    published = Column(Boolean, server_default=expression.true()) # This sets the default value at server level (schema)
    owner_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=expression.text('now()'))
    owner = Relationship("User")

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=expression.text('now()'))

class Vote(Base):
    __tablename__= "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), 
                     primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),
                     primary_key=True)