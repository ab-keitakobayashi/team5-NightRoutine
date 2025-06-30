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
    user_id = Column(String, nullable=False)
    write_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False)

class EfScoreSummary(BaseModel):
    ef_item_id: int
    total_score: int
    dates: List[str]

app = FastAPI()
@app.get("/user/{user_id}/ef_scores", response_model=List[EfScoreSummary])
def get_ef_score_summary(user_id: str, db: Session = Depends(get_db)):
    # ユーザー情報取得
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # ユーザーが登録したEF（nullを除外）
    user_ef_ids = [
        user.ef_item_id_1, user.ef_item_id_2, user.ef_item_id_3,
        user.ef_item_id_4, user.ef_item_id_5
    ]
    user_ef_ids = [eid for eid in user_ef_ids if eid is not None]

    # 全EF項目（1～7）を取得
    all_ef_ids = list(range(1, 8))

    # ユーザーが選択していないEFはクラスのEFとして扱う
    missing_ef_ids = [eid for eid in all_ef_ids if eid not in user_ef_ids]

    # 削除されていないレポートを取得
    reports = db.query(ReportsModel).filter(
        ReportsModel.user_id == user_id,
        ReportsModel.is_deleted == False
    ).all()
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

    # 返却用リストを作成（ユーザーEF＋未選択EF＝全7項目）
    result = []
    for ef_id in user_ef_ids + missing_ef_ids:
        if ef_id in ef_summary:
            data = ef_summary[ef_id]
            result.append(EfScoreSummary(
                ef_item_id=ef_id,
                total_score=data["total_score"],
                dates=data["dates"]
            ))
        else:
            result.append(EfScoreSummary(
                ef_item_id=ef_id,
                total_score=0,
                dates=[]
            ))
    return result