from fastapi import FastAPI,APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models import  ReportResponse# Userモデル
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from db_connect import get_db
from datetime import datetime
"""
DB接続設定とモデル定義
"""
# DB接続設定
router = APIRouter()
app = FastAPI()
Base = declarative_base()
class User(Base):
    __tablename__ = "testusers"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_mailAddress = Column(String, unique=True, nullable=False)
    class_id = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)
    avatar_id = Column(Integer, nullable=False)
    enemy_id = Column(Integer, nullable=False)
    enemy_hp = Column(Integer, nullable=False)
    ef_item_id_1 = Column(Integer, nullable=False)
    ef_item_id_2 = Column(Integer, nullable=False)
    ef_item_id_3 = Column(Integer, nullable=False)
    ef_item_id_4 = Column(Integer, nullable=False)
    ef_item_id_5 = Column(Integer, nullable=False)

class Report(BaseModel):

    start_time : str
    endTime : str
    successes: str
    failures : str
    tasks : str

class tasksModel(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer,  unique= True,nullable=True)#ForeignKey('reports.report_id'))
    start_time = Column(DateTime, nullable=False)
    task_description = Column(String, nullable=False)


class ReviewsModel(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, unique= True,nullable=True)#
    successes = Column(String, nullable=False)
    failures = Column(String, nullable=False)
    ai_comment = Column(String, nullable=False)

Base = declarative_base()
class ReportsModel(Base):
    __tablename__ = "reports"

    user_id = Column(Integer, unique= True,nullable=True)#ForeignKey('testusers.user_id'))
    report_id = Column(Integer, primary_key=True, index=False)
    write_date = Column(DateTime, default=datetime, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)  # 0: 未削除, 1: 削除済み   


# # ④itemを追加（サンプル実装済み）
@app.post("/report/regi/{user_id}/{day}", response_model=ReportResponse)
def registor_report(user_id: int, day: datetime, 
                    report: Report, db_session: Session = Depends(get_db)): 

    db_repo = ReportsModel(user_id = user_id, 
                           write_date = day, 
                           is_deleted = 0) #task_idは自動採番されるため、リクエストには含めない
    db_session.add(db_repo)
    print("db_repo", db_repo)
    db_session.commit()
    db_session.refresh(db_repo)

    db_task = tasksModel(
                           report_id = db_repo.report_id,
                           start_time = report.start_time, 
                           task_description = report.tasks)
    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)
    
    db_review = ReviewsModel(
                           report_id = db_repo.report_id,
                           successes = report.successes, 
                           failures = report.failures,
                           ai_comment = "AIのコメント")
    
    db_session.add(db_review)
    db_session.commit()
    db_session.refresh(db_review)

    return ReportResponse(user_id=user_id, 
                            report_id=db_repo.report_id, 
                            startTime=report.start_time, 
                            endTime=report.endTime, 
                            successes=report.successes, 
                            failures=report.failures,
                            tasks=report.tasks)  
#レビューを更新
@app.put("/report/regi/update/{user_id}/{day}")
def update_report(user_id: int, day: datetime, report: Report, db: Session = Depends(get_db)):
    db_repo = db.query(ReportsModel).filter(ReportsModel.user_id == user_id, ReportsModel.write_date == day).first()
    
    if not db_repo:
        print("db_repo not found")
        raise HTTPException(status_code=404, detail="Report not found")

    db_tasks = db.query(tasksModel).filter(tasksModel.report_id == db_repo.report_id).first()
    if not db_tasks:
        raise HTTPException(status_code=404, detail=f"{db_repo.report_id}Tasks not found")

    db_tasks.start_time = report.start_time
    db_tasks.task_description = report.tasks
    db.commit()
    db.refresh(db_tasks)

    db_review = db.query(ReviewsModel).filter(ReviewsModel.report_id == db_repo.report_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_review.successes = report.successes
    db_review.failures = report.failures
    db_review.ai_comment = "AIのコメント(updated)"
    db.commit()
    db.refresh(db_review)

    return db_review

#レビューを更新
@app.patch("/report/regi/update/{user_id}/{day}")
def update_report(user_id: int, day: datetime, report: Report, db: Session = Depends(get_db)):
    db_repo = db.query(ReportsModel).filter(ReportsModel.user_id == user_id, ReportsModel.write_date == day).first()
    
    if not db_repo:
        print("db_repo not found")
        raise HTTPException(status_code=404, detail="Report not found")

    db_repo.is_deleted = 1  # 1: 削除済み 
    db.session.commit()
    db.session.refresh(db_repo)

    return db_repo
