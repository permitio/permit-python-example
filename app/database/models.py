from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    email = Column(String, primary_key=True, index=True)
    hash_pwd = Column(String, nullable=False)
    name = Column(String, nullable=False)

     # One-to-many relationship with Comment
    designs = relationship('Design', back_populates='user', cascade="all, delete-orphan")

    # One-to-many relationship with Design
    comments = relationship('Comment', back_populates='user', cascade="all, delete-orphan")


class Design(Base):
    __tablename__ = 'design'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Assuming you want a title
    description = Column(String)  # Optional description

     # Many-to-one relationship with User
    user_email = Column(String, ForeignKey('user.email'), nullable=False)
    user = relationship('User', back_populates='designs')

    # One-to-many relationship with Comment
    comments = relationship('Comment', back_populates='design', cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)  # Assuming you want to store the content of the comment

   # Many-to-one relationship with Design
    design_id = Column(Integer, ForeignKey('design.id'), nullable=False)
    design = relationship('Design', back_populates='comments')
    
    # Many-to-one relationship with User
    user_email = Column(String, ForeignKey('user.email'), nullable=False)
    user = relationship('User', back_populates='comments')



