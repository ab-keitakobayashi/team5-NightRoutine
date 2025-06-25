from fastapi import FastAPI,APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models import Reports ,Report , ReportResponse# Userモデル
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


"""
DB接続設定とモデル定義
"""
# DB接続設定
DATABASE_URL = "mysql+pymysql://admin:fy26admin@fy26-training-handson-db.cxok2mc8wgeq.ap-northeast-1.rds.amazonaws.com:3306/handson"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

router = APIRouter()
app = FastAPI()

    
# データベースセッションをリクエストごとに取得するための依存関係を定義
# リクエスト処理が終わると自動でセッションを閉じる
def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()



# # ④itemを追加（サンプル実装済み）
@app.post("/report/regi/{user_id}/{day}", response_model=ReportResponse)
def registor_report(user_id: int, day: datetime, report: Report, db_session: Session = Depends(get_db_session)): 
#     # report = Reports(
#     #     startTime=0.0,
#     #     endTime=0.0,
#     #     successes="",
#     #     failures="",
#     #     tasks=""
#     # ) # idは自動採番されるため、リクエストには含めない
    db_item = Reports(startTime=report.startTime, endTime=report.endTime, successes=report.successes, failures=report.failures, tasks=report.tasks) # idは自動採番されるため、リクエストには含めない
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return ReportResponse(user_id=user_id, 
                            report_id=report.report_id, 
                            startTime=report.startTime, 
                            endTime=report.endTime, 
                            successes=report.successes, 
                            failures=report.failures,
                            tasks=report.tasks)  

# @app.post("/report/regi/{user_id}")
# def post_report(user_id: int):
#     return "aaaaaa"