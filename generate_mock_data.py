from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random

from app.database.crud import create_user, create_snake

# Import your models and schemas
from app.database.models import Base, User, Snake, Tank, SnakeType
from app.database.schemas import UserCreate, SnakeCreate

# Set up the database connection and session
DATABASE_URL = "postgresql://postgres:postgres@localhost/zoo"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Initialize Faker
fake = Faker()

def create_mock_user(db: Session):
    email = fake.email()
    name = fake.name()
    password = fake.password()
    user_create = UserCreate(email=email, name=name, password=password)
    return create_user(db, user_create)

def create_mock_tank(db: Session):
    tank = Tank()
    db.add(tank)
    db.commit()
    db.refresh(tank)
    return tank

def create_mock_snake(db: Session, tank_id: int, snake_id: int):
    snake_type = SnakeType.python
    snake_create = SnakeCreate(type=snake_type,id = snake_id, tank_id=tank_id)
    return create_snake(db, snake_create)

def main():
    # Create a database session
    db = SessionLocal()
    try:
        # Generate mock users
        for _ in range(5):
            user = create_mock_user(db)
            print(f"Created user: {user.email}")

        # Generate mock tanks and snakes
        for _ in range(3):
            tank = create_mock_tank(db)
            print(f"Created tank with ID: {tank.id}")
            for i in range(2):
                snake = create_mock_snake(db, tank.id, i  )
                print(f"Created snake of type {snake.type} in tank {snake.tank_id}")

    finally:
        db.close()

if __name__ == "__main__":
    main()
