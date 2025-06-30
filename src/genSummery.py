from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from db_connect import get_db  # DBセッション取得関数
from models import User, EfModel, ReviewsModel, ReportsModel, ef_items_data, reviews_aicomment_data,ScoresModel, SummaryRequest
import boto3
import json
from typing import List
import os
from typing import List, Dict, Any
from pydantic import BaseModel

Base = declarative_base()
app = FastAPI()

# 環境変数からAWS情報を取得
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")

    

class EfAssessmentSummary(BaseModel):
    ef_item_id: int
    total_score: int

# --- Bedrock Function ---
def post_efAssessment_from_bedrock(ef_input: List[ef_items_data], reviews_data: List[reviews_aicomment_data]) -> str:
    client = boto3.client(
        'bedrock-runtime',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME  # Bedrockのリージョン
    )

    prompt = (
        "あなたは評価項目をもとに一定期間の業務内容の振り返りへのフィードバックの要約をするAIです。\n"
        "評価項目は「項目番号：評価項目説明」の形式で与えられます。\n"
        "一日の業務内容の振り返りへのフィードバックは「生成メッセージ」の形式で与えられます。\n"
        "また、アドバイスを答えるときは評価項目に沿って答えてください。生成メッセージで触れられていない評価項目に関しては無視してください。\n"
    )

    for ef in ef_input:
        prompt += f"評価項目は「{ef.ef_item_id}:{ef.item}」です。\n"
    for r in reviews_data:
        prompt += f"一日の業務内容の振り返りへのフィードバックは「{r.ai_comment}」です。\n"

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=body
    )

    response_body = json.loads(response.get('body').read())
    print("Bedrockのレスポンス:", response_body)
    return response_body["content"][0]["text"]

# --- FastAPI Endpoint ---
@app.post("/user/{user_id}/reviews/")
def post_reviews_and_advice(user_id: str, request: SummaryRequest, db: Session = Depends(get_db)):
    report_ids = db.query(ReportsModel.report_id).filter(
        and_(
            ReportsModel.user_id == user_id,
            ReportsModel.write_date >= request.start_date,
            ReportsModel.write_date <= request.end_date,
            ReportsModel.is_deleted == False
        )
    ).all()
    report_ids = [r[0] for r in report_ids]
    if not report_ids:
        raise HTTPException(status_code=404, detail="No reports found")

    # 取得した report_ids を使って reviews を取得
    reviews = db.query(ReviewsModel).filter(
        ReviewsModel.report_id.in_(report_ids)
    ).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    selected_ef_ids = [
        user.ef_item_id_1,
        user.ef_item_id_2,
        user.ef_item_id_3,
        user.ef_item_id_4,
        user.ef_item_id_5
    ]
    ef_items_selected = db.query(EfModel).filter(EfModel.ef_item_id.in_(selected_ef_ids)).all()
    selected_categories = {ef.ef_category_id for ef in ef_items_selected}
    all_class_ef = db.query(EfModel).filter(EfModel.class_id == user.class_id).all()

    remaining_ef_items = []
    for ef in all_class_ef:
        if ef.ef_category_id not in selected_categories:
            remaining_ef_items.append(ef)
            selected_categories.add(ef.ef_category_id)
        if len(remaining_ef_items) == 2:
            break

    ef_items = ef_items_selected + remaining_ef_items

    ef_input_models = [ef_items_data(ef_item_id=e.ef_item_id, item=e.item) for e in ef_items]
    review_input_models = [reviews_aicomment_data(ai_comment=r.ai_comment) for r in reviews]

    assessment = post_efAssessment_from_bedrock(ef_input_models, review_input_models)

    # --- ここからスコア集計 ---
    # ScoresModelのimportが必要です
    from models import ScoresModel

    scores = db.query(ScoresModel).filter(ScoresModel.report_id.in_(report_ids)).all()
    ef_summary: Dict[int, int] = {}
    for s in scores:
        if s.ef_item_id not in ef_summary:
            ef_summary[s.ef_item_id] = 0
        ef_summary[s.ef_item_id] += s.score

    ef_assessment_summary = [
        EfAssessmentSummary(
            ef_item_id=ef_item_id,
            total_score=total_score
        )
        for ef_item_id, total_score in ef_summary.items()
    ]
    return {
        "assessment": assessment,
        "ef_assessment_summary": [e.model_dump() for e in ef_assessment_summary]
    }