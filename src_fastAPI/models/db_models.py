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
    __tablename__ = "group5_users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_mailAddress = Column(String, unique=True, nullable=False)
    class_id = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)
    avatar_id = Column(Integer, nullable=False)
    enemy_id = Column(Integer, nullable=False)
    enemy_hp = Column(Integer, nullable=False)
    ef_item_id1 = Column(Integer, nullable=False)
    ef_item_id2 = Column(Integer, nullable=False)
    ef_item_id3 = Column(Integer, nullable=False)
    ef_item_id4 = Column(Integer, nullable=False)
    ef_item_id5 = Column(Integer, nullable=False)