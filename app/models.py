# Every model represents a table in our database
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
from .database import Base
from sqlalchemy.orm import relationship

# class Post extends class Base -> define a model
class Post(Base):
    # Name of the table in our database
    __tablename__ = "posts"

# define the columns of the table
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    # Create column to connect as foreign key 
    # Must match the type of col id in table users
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Create another property for a post, in it is the SQLalchemy class User below
    # When we retrieve a post, this relationship will give us the owner field of the post
    # Which a User => Fetch the User based on owner_id of the post
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), 
                     primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), 
                     primary_key=True)