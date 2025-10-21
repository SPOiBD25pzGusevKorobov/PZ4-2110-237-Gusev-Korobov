import sqlalchemy
import pandas as pd
import pymysql
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+pymysql://j30084097:7f9vGAxSu@mysql.65e3ab49565f.hosting.myjino.ru:3306/j30084097_pz4-gusev-korobov-2110"
)
connection = engine.connect()
print(connection)
