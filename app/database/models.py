from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
import enum

class Base(DeclarativeBase):
    pass

class SnakeType(enum.Enum):
    python = "python"
    cobra = "cobra"
    viper = "viper"

class User(Base):
    __tablename__ = "user"
    email = Column(String, primary_key=True, index=True)
    hash_pwd = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Snake(Base):
    __tablename__ = 'snake'
    id = Column(Integer, primary_key=True)
    type = Column(SQLAEnum(SnakeType), nullable=False)
    tank_id = Column(Integer, ForeignKey('tank.id'), nullable=False)
    tank = relationship('Tank', back_populates='snakes')

class Tank(Base):
    __tablename__ = 'tank'
    id = Column(Integer, primary_key= True)
    snakes = relationship('Snake', back_populates='tank')

