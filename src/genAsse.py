from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_connect import get_db  # DBセッション取得関数
from models import User, UserResiResponse, UserResiRequest ,Ef_Items,EfModel , GenAsseResponse,GenAssessmentRequest# Userモデル
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import boto3
import json
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

Base = declarative_base()

# 環境変数からAWS情報を取得
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")

# class EfModel(Base):
#     __tablename__ = "ef_items" # テーブル名
#     ef_item_id = Column(Integer, primary_key=True) # 主キー
#     ef_category_id = Column(Integer, nullable=False) # カテゴリID
#     class_id = Column(Integer, nullable=False)
#     item = Column(String, nullable=False) # アイテム名

# class tasksModel(Base):
#     __tablename__ = "tasks"

#     task_id = Column(Integer, primary_key=True, index=True)
#     report_id = Column(Integer,  unique= True,nullable=True)#ForeignKey('reports.report_id'))
#     start_time = Column(DateTime, nullable=False)
#     task_description = Column(String, nullable=False)


# class ReviewsModel(Base):
#     __tablename__ = "reviews"

#     review_id = Column(Integer, primary_key=True, index=True)
#     report_id = Column(Integer, unique= True,nullable=True)#
#     successes = Column(String, nullable=False)
#     failures = Column(String, nullable=False)
#     ai_comment = Column(String, nullable=False)

# Base = declarative_base()
# class ReportsModel(Base):
#     __tablename__ = "reports"

#     user_id = Column(Integer, unique= True,nullable=True)#ForeignKey('testusers.user_id'))
#     report_id = Column(Integer, primary_key=True, index=False)
#     write_date = Column(DateTime, default=datetime, nullable=False)
#     is_deleted = Column(Boolean, default=0, nullable=False)  # 0: 未削除, 1: 削除済み  
 
# class Report(BaseModel):
 
#     start_time : str
#     endTime : str
#     successes: str
#     failures : str

# #pythonモデル
# class Ef_Items(BaseModel):
#     ef_item_id: int
#     ef_category_id: int
#     class_id: int
#     item: str

# class Tasks(BaseModel):
#     task_id: int
#     report_id: int
#     start_time: str
#     task_description: str

# class Review(BaseModel):
#     review_id: int
#     report_id: int
#     successes: str
#     failures: str
#     ai_comment: str

# class GenAssessmentRequest(BaseModel):
#     start_time: list[str]
#     task_description: list[str]
#     success: str
#     failure: str
# # レスポンスモデル
# class GenAsseResponse(BaseModel):
#     ef_plus_points: list[int]  # EF項目のIDのリスト
#     ef_minus_points: list[int]  # マイナスEF項目のIDのリスト
#     assessment: str  # AIからのアドバイス
    
# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

 # 3. EFModelの内容を取得（ユーザーが選択した5つ＋職位に紐づく残り2つ）
def get_ef_items(db, user_id: int):
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
    # 職位(class_id)に紐づく全EFのうち、未選択のef_category_idごとに1つだけ取得

    # すでに選択済みのef_category_idを取得
    selected_categories = set()
    for ef in ef_items_selected:
        selected_categories.add(ef.ef_category_id)

    # 現在の職位(class_id)に紐づくEFから、未選択のカテゴリのみを抽出
    all_class_ef = db.query(EfModel).filter(EfModel.class_id == user.class_id).all()
    remaining_ef_items = []
    for ef in all_class_ef:
        if ef.ef_category_id not in selected_categories:
            remaining_ef_items.append(ef)
    selected_categories.add(ef.ef_category_id)  # 1カテゴリにつき1つだけ

    # 2つまで取得
    remaining_ef_items = remaining_ef_items[:2]
    # 合成（合計7件になる想定）
    ef_items_all = ef_items_selected + remaining_ef_items
    return ef_items_all

# Bedrockを使用してEFとユーザー入力をもとに一致するEF項目を出力する
def get_efPoint_from_bedrock(ef_items_all: list[EfModel], start_times: list[str], task_descriptions: list[str], user_input: str, success: bool) -> list[int]:
    client = boto3.client(
        'bedrock-runtime',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    prompt = (
        "あなたは評価項目をもとに一日の業務内容から当てはまる項目を判定するAIです。\n"
        "評価項目は「評価項目名番号：評価項目説明」の形式で与えられます。\n"
        "一日の業務内容は「開始時間：業務内容」の形式で与えられます。\n"
        "また、当てはまる項目を答えるときは「項目名番号」だけ答えてください。\n"
        "例：「1 3 5 7 9」"
    )

    # ここを修正
    for ef in ef_items_all:
        prompt += f"\n評価項目は「{ef.ef_category_id}:{ef.item}」です。"

    for time, task in zip(start_times, task_descriptions):
        prompt += f"\n開始時間と業務内容は「{time}:{task}」です。"
    if success:
        prompt += f"\n一日の業務内容でよかったことは「{user_input}」です。"
    else:
        prompt += f"\n一日の業務内容でわるかったことは「{user_input}」です。"
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=body
    )
    response_body = json.loads(response.get('body').read())
    answer = response_body["content"][0]["text"]
    answer = [int(x) for x in answer.split() if x.isdigit()]
    return answer

# Bedrockを使用してEFとユーザー入力をもとにassessmentを出力する
def get_efAssement_from_bedrock(ef_items_all: list[EfModel], start_times: list[str], task_descriptions: list[str], success: str, failure: str) -> str:
    client = boto3.client(
        'bedrock-runtime',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    prompt = (
        "あなたは評価項目をもとに一日の業務内容の振り返り（よかったこと、わるかったこと）からアドバイスをするAIです。\n"
        "評価項目は「評価項目名番号：評価項目説明」の形式で与えられます。\n"
        "一日の業務内容は「開始時間：業務内容」の形式で与えられます。\n"
        "また、アドバイスを答えるときは評価項目に沿って答えてください。\n"
    )
    # ここを修正
    for ef in ef_items_all:
        prompt += f"評価項目は「{ef.ef_category_id}:{ef.item}」です。\n"
    for time, task in zip(start_times, task_descriptions):
        prompt += f"開始時間と業務内容は「{time}:{task}」です。\n"
    prompt += f"一日の業務内容でよかったことは「{success}」です。\n"
    prompt += f"一日の業務内容でわるかったことは「{failure}」です。\n"

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=body
    )
    response_body = json.loads(response.get('body').read())
    answer = response_body["content"][0]["text"]
    return answer

@app.post("/user/{user_id}/assessment", response_model=GenAsseResponse)
def genasssessment(
    user_id: int,
    request: GenAssessmentRequest,
    db_session: Session = Depends(get_db)
):
    """
    ユーザーの業務内容をもとに評価項目を生成するエンドポイント
    :param user_id: ユーザーID
    :param user_input: ユーザーの業務内容
    :param db_session: データベースセッション
    :return: 評価項目のリスト
    """
    ef_items_all = get_ef_items(db_session, user_id)
    ef_plus_points = []
    ef_minus_points = []
    # ユーザー入力をもとにEF項目を取得
    ef_plus_points = get_efPoint_from_bedrock(ef_items_all, request.start_time, request.task_description, request.success, True)
    ef_minus_points = get_efPoint_from_bedrock(ef_items_all, request.start_time, request.task_description, request.failure, False)
    # EF項目のリストを返す
    assessment = get_efAssement_from_bedrock(ef_items_all, request.start_time, request.task_description, request.success, request.failure)
    return GenAsseResponse(
        ef_plus_points=ef_plus_points,
        ef_minus_points=ef_minus_points,
        assessment=assessment
    )