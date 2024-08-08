from sqlalchemy.orm import Session

from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hash_pwd=fake_hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_tank(db: Session, tank: schemas.TankCreate):
    db_tank = models.Tank()
    db.add(db_tank)
    db.commit()
    db.refresh(db_tank)

def create_snake(db: Session, snake: schemas.SnakeCreate):
    db_snake = models.Snake(id=snake.id, type=snake.type, tank_id=snake.tank_id)
    db.add(db_snake)
    db.commit()
    db.refresh(db_snake)

