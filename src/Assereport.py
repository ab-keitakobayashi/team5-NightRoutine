from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float,Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel,Base
from db_connect import get_db  # DBセッション取得関数
import requests
from fastapi import Body, FastAPI
from pydantic import BaseModel
from models import User
import boto3
import json


#リクエスト/レスポンススキーマ定義
class AssessmentReportRequest(BaseModel):
    startDate: int  # 期間（整数値）
    endDate: int  # 期間（整数値）

class AssessmentReportResponse(BaseModel):
    message: str  # レスポンスメッセージ


# DBモデル定義
class EfModel(Base):
    __tablename__ = "ef_items" # テーブル名
    ef_item_id = Column(Integer, primary_key=True) # 主キー
    ef_category_id = Column(Integer, nullable=False) # カテゴリID
    class_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False) # アイテム名

class ReviewsModel(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, unique= True,nullable=True)#
    successes = Column(String, nullable=False)
    failures = Column(String, nullable=False)
    ai_comment = Column(String, nullable=False)

class ReportsModel(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    write_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False)

class Report(BaseModel):

    start_time : str
    endTime : str
    successes: str
    failures : str
    tasks : str


# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

from datetime import date
from sqlalchemy import and_

@app.get("/user/{user_id}/reviews/")
def get_reviews_and_advice(
    user_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    # 1. 指定期間のreport_idを取得
    report_ids = db.query(ReportsModel.report_id).filter(
        and_(
            ReportsModel.user_id == user_id,
            ReportsModel.write_date >= start_date,
            ReportsModel.write_date <= end_date,
            ReportsModel.is_deleted == False
        )
    ).all()
    report_ids = [r[0] for r in report_ids]
    if not report_ids:
        raise HTTPException(status_code=404, detail="No reports found")

    # 2. reviewsを取得
    reviews = db.query(ReviewsModel).filter(
        ReviewsModel.report_id.in_(report_ids)
    ).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    # 3. EFModelの内容を取得（ユーザーが選択した5つ＋職位に紐づく残り2つ）

    # ユーザー情報を取得
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ユーザーが選択した5つのef_item_id
    selected_ef_ids = [
        user.ef_item_id_1,
        user.ef_item_id_2,
        user.ef_item_id_3,
        user.ef_item_id_4,
        user.ef_item_id_5
    ]
    # 5つのEF（ユーザーが選択したもの）
    ef_items_selected = db.query(EfModel).filter(EfModel.ef_item_id.in_(selected_ef_ids)).all()

    # 職位(class_id)に紐づく全EFのうち、未選択のものから2つ取得
    all_class_ef = db.query(EfModel).filter(EfModel.class_id == user.class_id).all()
    remaining_ef_items = [e for e in all_class_ef if e.ef_item_id not in selected_ef_ids][:2]

    # 合成（合計7件になる想定）
    ef_items = ef_items_selected + remaining_ef_items

    # 4. Bedrockに送るデータを整形
    reviews_data = [
        {
            "successes": r.successes,
            "failures": r.failures,
            "ai_comment": r.ai_comment
        }
        for r in reviews
    ]
    ef_items_data = [
        {
            "ef_item_id": e.ef_item_id,
            "item": e.item
        }
        for e in ef_items
    ]

    # 5. Bedrockに送信（例：関数呼び出し）
    advice = get_advice_from_bedrock(reviews_data, ef_items_data)

    return {
        "reviews": reviews_data,
        "advice": advice
    }

# Bedrock連携の例
def get_advice_from_bedrock(reviews, ef_items):
    # ここでBedrock APIにリクエストを送り、アドバイスを生成
    # 例: boto3やrequestsでAPI呼び出し
    # 今回はダミーで返す
    return "ここにAIによるアドバイスが入ります"






