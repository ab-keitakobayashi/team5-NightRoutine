from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

"""
DB接続設定とモデル定義
"""
# DB接続設定
DATABASE_URL = "mysql+pymysql://admin:fy26admin@fy26-training-handson-db.cxok2mc8wgeq.ap-northeast-1.rds.amazonaws.com:3306/handson" ##URL
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemModel(Base):
    __tablename__ = "group5_users_test" # テーブル名
    id = Column(Integer, primary_key=True) # 主キー
    name = Column(String, index=True)
    price = Column(Float)