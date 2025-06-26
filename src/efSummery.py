from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from db_connect import get_db  # DBセッション取得関数
from models import User
import boto3
import json
from typing import Any, Dict, List

Base = declarative_base()

# SQLAlchemyモデル例（必要に応じて修正してください）
class ScoresModel(Base):
    __tablename__ = "scores"
    score_id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer, nullable=False)
    ef_item_id = Column(Integer, nullable=False)
    report_id = Column(Integer, nullable=False)

class ReportsModel(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    write_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False)

class EfScoreSummary(BaseModel):
    ef_item_id: int
    total_score: int
    dates: List[str]

app = FastAPI()
@app.get("/user/{user_id}/ef_scores", response_model=List[EfScoreSummary])
def get_ef_score_summary(user_id: int, db: Session = Depends(get_db)):
    # 削除されていないレポートを取得
    reports = db.query(ReportsModel).filter(
        ReportsModel.user_id == user_id,
        ReportsModel.is_deleted == False
    ).all()
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found for this user.")

    report_id_to_date = {r.report_id: r.write_date.strftime("%Y-%m-%d") for r in reports}
    report_ids = list(report_id_to_date.keys())

    # scoresテーブルから該当するスコアを取得
    scores = db.query(ScoresModel).filter(ScoresModel.report_id.in_(report_ids)).all()

    ef_summary: Dict[int, Dict[str, Any]] = {}
    for s in scores:
        if s.ef_item_id not in ef_summary:
            ef_summary[s.ef_item_id] = {"total_score": 0, "dates": []}
        ef_summary[s.ef_item_id]["total_score"] += s.score
        ef_summary[s.ef_item_id]["dates"].append(report_id_to_date[s.report_id])

    # 整形して返却
    result = [
        EfScoreSummary(
            ef_item_id=ef_item_id,
            total_score=data["total_score"],
            dates=data["dates"]
        )
        for ef_item_id, data in ef_summary.items()
    ]
    return result