from fastapi import FastAPI,APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models import  EfModel,ReportResponse,ReportRegiResponse, Report, User, ReportsModel,tasksModel,ReviewsModel,Review # Userモデル
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from db_connect import get_db
from datetime import datetime
from typing import List
import requests
"""
DB接続設定とモデル定義
"""

# DB接続設定
router = APIRouter()
app = FastAPI()
Base = declarative_base()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 必要に応じて追加
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class User(Base):
#     __tablename__ = "testusers"

#     user_id = Column(Integer, primary_key=True, index=True)
#     user_name = Column(String, nullable=False)
#     user_mailAddress = Column(String, unique=True, nullable=False)
#     class_id = Column(Integer, nullable=False)
#     period = Column(Integer, nullable=False)
#     avatar_id = Column(Integer, nullable=False)
#     enemy_id = Column(Integer, nullable=False)
#     enemy_hp = Column(Integer, nullable=False)
#     ef_item_id_1 = Column(Integer, nullable=False)
#     ef_item_id_2 = Column(Integer, nullable=False)
#     ef_item_id_3 = Column(Integer, nullable=False)
#     ef_item_id_4 = Column(Integer, nullable=False)
#     ef_item_id_5 = Column(Integer, nullable=False)

# class Report(BaseModel):
#     start_time: List[str]
#     # endTime: List[str]
#     successes: str
#     failures: str
#     tasks: List[str] 

# class ReportResponse(BaseModel):
    
#     start_time: List[str]  # タスクの開始時間のリスト
#     successes: str  # 成功したタスクの説明
#     failures: str  # 失敗したタスクの説明
#     assessments_points: dict  # レポートの詳細データ
#     assessment: str
#     tasks: List[str]  # タスクの説明
#     # user_id: int
#     # report_id: int
#     # start_time: List[str]
#     # # endTime: List[str]
#     # successes: str
#     # failures : str
#     # tasks: List[str]

# class tasksModel(Base):
#     __tablename__ = "tasks"

#     task_id = Column(Integer, primary_key=True, index=True)
#     report_id = Column(Integer,  unique= True,nullable=True)#ForeignKey('reports.report_id'))
#     start_time = Column(String, nullable=False)
#     task_description = Column(String, nullable=False)

# class Ef_Items(Base):
#     __tablename__ = "ef_items"

#     ef_item_id = Column(Integer, primary_key=True, index=True)
#     ef_category_id = Column(Integer, nullable=False)
#     class_id = Column(Integer, nullable=False)
#     item = Column(String, nullable=False)

# class ReviewsModel(Base):
#     __tablename__ = "reviews"

#     review_id = Column(Integer, primary_key=True, index=True)
#     report_id = Column(Integer, unique= True,nullable=True)#
#     successes = Column(String, nullable=False)
#     failures = Column(String, nullable=False)
#     ai_comment = Column(String, nullable=False)


# class ReportsModel(Base):
#     __tablename__ = "reports"

#     user_id = Column(Integer, unique= True,nullable=True)#ForeignKey('testusers.user_id'))
#     report_id = Column(Integer, primary_key=True, index=False)
#     write_date = Column(DateTime, default=datetime, nullable=False)
#     is_deleted = Column(Integer, default=0, nullable=False)  # 0: 未削除, 1: 削除済み   


# bedrock生成文を取得
def get_assessment_url(user_id: int, payload: dict = None) -> dict:
    """
    指定したユーザーIDに対して、JSON形式のデータをPOSTし、評価情報を取得します。
    payload: dict型で渡すデータ（例: {"key": "value"}）
    """
    url = f"http://127.0.0.1:8000/user/{user_id}/assessment"
    if payload is None:
        payload = {}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("data-------------",data)
        return {
            "ef_plus_points": data.get('ef_plus_points'),
            "ef_minus_points": data.get('ef_minus_points'),
            "assessment": data.get('assessment'),
        }
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to get assessment")

# アセスメントのデータ成型
def generate_assessments_points(output_assessments):
    assessments_points = []
    for ef_id in output_assessments.get("ef_plus_points", []):
        assessments_points.append({"EF_id": ef_id, "score": 1})
    for ef_id in output_assessments.get("ef_minus_points", []):
        assessments_points.append({"EF_id": ef_id, "score": -1})
    return assessments_points


def replace_ef_id_with_item(assessments_points, db_session):
    result = []
    for ap in assessments_points:
        ef_item = db_session.query(EfModel).filter(EfModel.ef_item_id == ap['EF_id']).first()
        if ef_item:
            # 例: ef_item.ef_item_name を使う場合
            result.append({'item': ef_item.item, 'score': ap['score']})
        else:
            # 見つからない場合はそのままEF_idを使うなど
            result.append({'item': ap['EF_id'], 'score': ap['score']})
    return result

# # ④itemを追加（サンプル実装済み）
@app.post("/report/{user_id}/{day}/regi")#, response_model=ReportResponse)
def registor_report(user_id: int, day: datetime, 
                    report: Report, db_session: Session = Depends(get_db)): 
    reportdata = {
            "start_time": report.start_time,
            "task_description": report.tasks,
            "success": report.successes,
            "failure": report.failures
        }
    
    output_assessments = get_assessment_url(user_id, reportdata)
    assessments_points = generate_assessments_points(output_assessments)
    assessments_points = replace_ef_id_with_item(assessments_points, db_session)

    db_repo = ReportsModel(user_id = user_id, 
                           write_date = day, 
                           is_deleted = 0) #task_idは自動採番されるため、リクエストには含めない
    db_session.add(db_repo)
    print("db_repo", db_repo)
    db_session.commit()
    db_session.refresh(db_repo)

    # start_timeとtasksは2次元配列なので、先頭から取り出して登録
    for i in range(min(len(report.start_time), len(report.tasks))):
        start_time_item = report.start_time[i] if report.start_time else None
        print("start_time_item", start_time_item)
        task_description_item = report.tasks[i] if report.tasks else None
        db_task = tasksModel(
            report_id=db_repo.report_id,
            start_time=start_time_item,
            task_description=task_description_item
        )
        db_session.add(db_task)
        db_session.commit()
    
    db_review = ReviewsModel(
                           report_id = db_repo.report_id,
                           successes = report.successes, 
                           failures = report.failures,
                           ai_comment = "AIのコメント")
    
    db_session.add(db_review)
    db_session.commit()
    db_session.refresh(db_review)
    print("db_review", db_review)
    return ReportRegiResponse(
            start_time=report.start_time,
            successes=report.successes,
            failures=report.failures,
            assessment=output_assessments
            )  
    
#レビューを更新
@app.put("/report/regi/{user_id}/{day}/update")
def update_report(user_id: int, day: datetime, report: Report, db: Session = Depends(get_db)):
    db_repo = db.query(ReportsModel).filter(ReportsModel.user_id == user_id, ReportsModel.write_date == day).all()
    
    if not db_repo:
        print("db_repo not found")
        raise HTTPException(status_code=404, detail="Report not found")

    db_tasks = db.query(tasksModel).filter(tasksModel.report_id == db_repo.report_id).all()
    if not db_tasks:
        raise HTTPException(status_code=404, detail=f"{db_repo.report_id}Tasks not found")

    db_tasks.start_time = report.start_time
    db_tasks.task_description = report.tasks
    db.commit()
    db.refresh(db_tasks)

    db_review = db.query(ReviewsModel).filter(ReviewsModel.report_id == db_repo.report_id).all()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_review.successes = report.successes
    db_review.failures = report.failures
    db_review.ai_comment = "AIのコメント(updated)"
    db.commit()
    db.refresh(db_review)

    return db_review

#レビューを削除
@app.patch("/report/regi/{user_id}/{day}/delete")
def update_report(user_id: int, day: datetime, db: Session = Depends(get_db)):
    db_repo = db.query(ReportsModel).filter(ReportsModel.user_id == user_id, ReportsModel.write_date == day).all()
    
    if not db_repo:
        print("db_repo not found")
        raise HTTPException(status_code=404, detail="Report not found")

    db_repo.is_deleted = 1  # 1: 削除済み 
    db.commit()
    db.refresh(db_repo)
    return db_repo

#レビューを取得
@app.post("/report/{user_id}/{day}/get")
def get_report(user_id: int, day: datetime,  db: Session = Depends(get_db)):
    print("now finding")
    db_repo = db.query(ReportsModel).filter(ReportsModel.user_id == user_id, ReportsModel.write_date == day).first()
    print("now finded")
    print(db_repo.report_id)

    if not db_repo:
        print("db_repo not found")
        raise HTTPException(status_code=404, detail="Report not found")

    db_tasks = db.query(tasksModel).filter(tasksModel.report_id == db_repo.report_id).all()
    print("db_tasks", db_tasks)
    if not db_tasks:
        raise HTTPException(status_code=404, detail=f"{db_repo.report_id}Tasks not found")


    db_review = db.query(ReviewsModel).filter(ReviewsModel.report_id == db_repo.report_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    start_times = [task.start_time for task in db_tasks]
    print(start_times)
    print(db_review.successes)
    print(db_review.failures)

    return ReportResponse(
            start_time=start_times,
            successes=db_review.successes,
            failures=db_review.failures,
            tasks=[task.task_description for task in db_tasks],
            assessments = {
                "items": [
                    { "EF_item": "自己管理", "score": 10, "total_score": 10 },
                    { "EF_item": "注意力", "score": -10, "total_score": 8 },
                    { "EF_item": "感情制御", "score": -10, "total_score": 9 },
                    { "EF_item": "計画性", "score": 10, "total_score": 7 },
                    { "EF_item": "柔軟性", "score": 10, "total_score": 12 },
                ],
                "assessment":
                    "本日の業務は全体的に良好でしたが、注意力に関しては改善の余地があります。特に、タスクの切り替え時に集中力を欠くことがありました。次回は、タスクごとに短い休憩を挟むことで、注意力を高めることをお勧めします。",
            })
    
#レビューを一時保存
@app.post("/report/{user_id}/{day}/save")
def save_report(user_id: int, day: datetime, report: Report, db_session: Session = Depends(get_db)):
    db_repo = db_session.query(ReportsModel).filter(ReportsModel.user_id == user_id, ReportsModel.write_date == day).all()

    if not db_repo:

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
        db_tasks = db_session.query(tasksModel).filter(tasksModel.report_id == db_repo.report_id).all()
    else:
        db_tasks = db_session.query(tasksModel).filter(tasksModel.report_id == db_repo.report_id).all()
        if not db_tasks:
            raise HTTPException(status_code=404, detail=f"{db_repo.report_id}Tasks not found")

        db_tasks.start_time = report.start_time
        db_tasks.task_description = report.tasks
        db_session.commit()
        db_session.refresh(db_tasks)

        db_review = db_session.query(ReviewsModel).filter(ReviewsModel.report_id == db_repo.report_id).all()
        if not db_review:
            raise HTTPException(status_code=404, detail="Review not found")

        db_review.successes = report.successes
        db_review.failures = report.failures
        db_review.ai_comment = "AIのコメント(updated)"
        db_session.commit()
        db_session.refresh(db_review)

    return db_repo