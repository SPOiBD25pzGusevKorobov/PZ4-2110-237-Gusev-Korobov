import sqlalchemy
import pandas as pd
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text
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

def drop_table(table_name):
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`;"))
        print(f"Таблица '{table_name}' удалена (если существовала).")

def drop_table_static():
    Base.metadata.drop_all(engine)
    print("Таблица удалена.")

def show_table(table_name, limit=10):
    df = pd.read_sql_query(f"SELECT * FROM `{table_name}` LIMIT {limit}", con=engine)
    print(df)


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

def update_user_all(user_id, name, email, birthdate, is_active, phone, city):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.name = name
        user.email = email
        user.birthdate = birthdate
        user.is_active = is_active
        user.phone = phone
        user.city = city
        session.commit()
        print(f"Пользователь с id={user_id} обновлен полностью:")
        print(user.id, user.name, user.email, user.birthdate, user.is_active, user.phone, user.city)
    else:
        print(f"Пользователь с id={user_id} не найден.")
        session.close()

def export_to_csv(filename):
    session = Session()
    df = pd.read_sql(session.query(User).statement, session.bind)
    df.to_csv(filename, index=False)
    print(f"Данные экспортированы в {filename}")
    session.close()

def import_csv(csv_path, table_name=None):
    df = pd.read_csv(csv_path)
    print("Столбцы файла:", df.columns.tolist())
    if table_name is None:
        import os
        table_name = os.path.splitext(os.path.basename(csv_path))[0]
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"CSV-таблица '{csv_path}' импортирована в таблицу MySQL '{table_name}'")


create_table()
insert_users()
update_user_all(
    user_id=1,
    name="Иван Петров",
    email="ivanpetrov@example.com",
    birthdate=date(1991, 2, 2),
    is_active=False,
    phone="999999999",
    city="Екатеринбург"
)
select_all()
export_to_csv("users1.csv")
df = pd.read_csv("users1.csv")
print(df)
import_csv('diabetes.csv', table_name='diabetes')
export_to_csv('diabetes.csv')
drop_table('diabetes')
show_table('diabetes')


connection = engine.connect()
print(connection)
