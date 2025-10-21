import sqlalchemy
import pandas as pd
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date
engine = create_engine(
    "mysql+pymysql://j30084097:7f9vGAxSu@mysql.65e3ab49565f.hosting.myjino.ru:3306/j30084097_pz4-gusev-korobov-2110"
)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120))
    birthdate = Column(Date)
    is_active = Column(Boolean, default=True)
    phone = Column(String(20))
    city = Column(String(50))

def create_table():
    Base.metadata.create_all(engine)
    print("Таблица создана.")

def drop_table():
    Base.metadata.drop_all(engine)
    print("Таблица удалена.")

def insert_users():
    session = Session()
    users = [
        User(name="Иван Иванов", email="ivan@example.com", birthdate=date(1990, 1, 1), is_active=True,
             phone="1234567890", city="Москва"),
        User(name="Анна Петрова", email="anna@example.com", birthdate=date(1985, 6, 15), is_active=False,
             phone="0987654321", city="Санкт-Петербург"),
        User(name="Павел Сидоров", email="pavel@example.com", birthdate=date(2000, 12, 31), is_active=True,
             phone="5555555555", city="Казань")
    ]
    session.add_all(users)
    session.commit()
    print("Добавлены пользователи:")
    for user in users:
        print(user.name, user.email, user.birthdate, user.is_active, user.phone, user.city)
    session.close()

def select_all():
    session = Session()
    users = session.query(User).all()
    print("Текущий список пользователей:")
    for u in users:
        print(u.id, u.name, u.email, u.birthdate, u.is_active, u.phone, u.city)
    session.close()

drop_table()
create_table()
insert_users()
select_all()


connection = engine.connect()
print(connection)
