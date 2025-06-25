from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

"""
DB接続設定とモデル定義
"""
# DB接続設定
DATABASE_URL = "aws-handson-db-group-5.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com" ##URL
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
