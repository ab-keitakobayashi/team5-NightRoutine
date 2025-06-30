from fastapi import FastAPI

from models import  ReportResponse, Report, User, ReportsModel,tasksModel,ReviewsModel,Review,GenAsseResponse,GenAssessmentRequest,UserResiResponse, UserResiRequest, UserUpdateRequest, SummaryRequest
from reports_regi import registor_report,update_report, get_report, save_report
from genAsse import genasssessment
from regi import create_item
from renew import update_user_profile
from genSummery import post_reviews_and_advice
from fastapi import Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware  


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 必要に応じて追加
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from db_connect import get_db  # データベースセッション取得関数を用意してください

@app.post("/report/{user_id}/{day}/regi")
def Report_regi(user_id: str, day: datetime, report: Report, db_session: Session = Depends(get_db)):
    return registor_report(user_id, day, report, db_session)

#レビューを更新
@app.put("/report/{user_id}/{day}/update")
def Update_report(user_id: str, day: datetime, report: Report, db: Session = Depends(get_db)):
    return update_report(user_id, day, report, db)

@app.post("/report/{user_id}/{day}/get")
def Get_report(user_id: str, day: datetime,  db: Session = Depends(get_db)):
    return get_report(user_id, day, db)


#レビューを一時保存
@app.post("/report/{user_id}/{day}/save")
def Save_report(user_id: str, day: datetime, report: Report, db_session: Session = Depends(get_db)):
    return save_report(user_id, day, report, db_session)

#アセスメント生成AI
@app.post("/user/{user_id}/assessment", response_model=GenAsseResponse)
def Genasssessment(
    user_id: str,
    request: GenAssessmentRequest,
    db_session: Session = Depends(get_db)
):
    return genasssessment(user_id, request, db_session)


@app.post("/user/regi", response_model=UserResiResponse)
def Create_item(user: UserResiRequest, db_session: Session = Depends(get_db)):
    return create_item(user, db_session)


@app.put("/user/update/{user_id}", response_model=dict)
def Update_user_profile(user_id: str, request: UserUpdateRequest, db: Session = Depends(get_db)):
    return update_user_profile(user_id, request, db)

@app.post("/user/{user_id}/reviews/")
def Post_reviews_and_advice(user_id: str, request: SummaryRequest, db: Session = Depends(get_db)):
    return post_reviews_and_advice(user_id, request, db)