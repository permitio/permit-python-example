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

class Design(Base):
    __tablename__ = 'design'
    id = Column(Integer, primary_key= True)
    comments = relationship('Comment', back_populates='design')

class Comment(Base):
    __tablename__ = 'snake'
    id = Column(Integer, primary_key=True)
    design_id = Column(Integer, ForeignKey('design.id'), nullable=False)
    design = relationship('Design', back_populates='comments')



