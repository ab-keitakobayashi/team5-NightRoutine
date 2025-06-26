from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel,Base
from db_connect import get_db  # DBセッション取得関数
import requests
from fastapi import Body, FastAPI
from pydantic import BaseModel
import boto3
import json


#リクエスト/レスポンススキーマ定義
class AssessmentReportRequest(BaseModel):
    startDate: int  # 期間（整数値）
    endDate: int  # 期間（整数値）

class AssessmentReportResponse(BaseModel):
    message: str  # レスポンスメッセージ


# DBモデル定義
class efInfo(Base):
    __tablename__ = "ef_items" # テーブル名
    ef_item_id = Column(Integer, primary_key=True) # 主キー
    ef_category_id = Column(Integer, nullable=False) # カテゴリID
    class_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False) # アイテム名

class reviewsInfo(Base):
    __tablename__ = "reviews" # テーブル名
    review_id = Column(Integer, primary_key=True) # 主キー
    report_id = Column(Integer, nullable=False) # レポートID
    successes = Column(String, nullable=False) # 成功事例
    failures = Column(String, nullable=False) # 失敗事例
    ai_comment = Column(String, nullable=False) # AIコメント


# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

def get_assessment_report_from_bedrock(start_date: int, end_date: int) -> str:
   






