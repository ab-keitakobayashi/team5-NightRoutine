from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from typing import List
# """
# DB接続設定とモデル定義
# """
# # DB接続設定
# DATABASE_URL = "mysql+pymysql://admin:fy26admin@fy26-training-handson-db.cxok2mc8wgeq.ap-northeast-1.rds.amazonaws.com:3306/handson" ##URL
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# モデル定義
# データベースのテーブルを定義するためのモデルクラスを作成します。


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
    start_time: List[str]
    # endTime: List[str]
    successes: str
    failures: str
    tasks: List[str] 


class ReportResponse(BaseModel):
    
    start_time: List[str]  # タスクの開始時間のリスト
    successes: str  # 成功したタスクの説明
    failures: str  # 失敗したタスクの説明
    tasks: List[str]  # タスクの説明

class ReportRegiResponse(BaseModel):
    
    start_time: List[str]  # タスクの開始時間のリスト
    successes: str  # 成功したタスクの説明
    failures: str  # 失敗したタスクの説明
    assessment: dict  # レポートの詳細データ
    #assessment: str

    #tasks: List[str]  # タスクの説明

    # user_id: int
    # report_id: int
    # start_time: List[str]
    # # endTime: List[str]
    # successes: str
    # failures : str
    # tasks: List[str]

class tasksModel(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer,  unique= True,nullable=True)#ForeignKey('reports.report_id'))
    start_time = Column(String, nullable=False)
    task_description = Column(String, nullable=False)

# class Ef_Items(Base):
#     __tablename__ = "ef_items"

#     ef_item_id = Column(Integer, primary_key=True, index=True)
#     ef_category_id = Column(Integer, nullable=False)
#     class_id = Column(Integer, nullable=False)
#     item = Column(String, nullable=False)

class ReviewsModel(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, unique= True,nullable=True)#
    successes = Column(String, nullable=False)
    failures = Column(String, nullable=False)
    ai_comment = Column(String, nullable=False)


class ReportsModel(Base):
    __tablename__ = "reports"

    user_id = Column(Integer, unique= True,nullable=True)#ForeignKey('testusers.user_id'))
    report_id = Column(Integer, primary_key=True, index=False)
    write_date = Column(DateTime, default=datetime, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)  # 0: 未削除, 1: 削除済み   

# Pydanticモデル
# データのバリデーションとシリアライズを行うためのモデル]

# Post


class UserUpdateRequest(BaseModel):
    class_id: int
    period: int
    ef_item_id_1: int
    ef_item_id_2: int
    ef_item_id_3: int
    ef_item_id_4: int
    ef_item_id_5: int




class UserResiRequest(BaseModel):
    name: str
    mailAddress: str
    class_id: int
    period: int
    ef_item_id_1: int
    ef_item_id_2: int
    ef_item_id_3: int
    ef_item_id_4: int
    ef_item_id_5: int

class UserResiResponse(BaseModel):
    id: int
    name: str
    mailAddress: str
    class_id: int
    period: int
    avatar_id: int
    enemy_id: int
    enemy_hp: int
    ef_item_id_1: int
    ef_item_id_2: int
    ef_item_id_3: int
    ef_item_id_4: int
    ef_item_id_5: int

 
 
class EfModel(Base):
    __tablename__ = "ef_items" # テーブル名
    ef_item_id = Column(Integer, primary_key=True) # 主キー
    ef_category_id = Column(Integer, nullable=False) # カテゴリID
    class_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False) # アイテム名
 
#pythonモデル
class Ef_Items(BaseModel):
    ef_item_id: int
    ef_category_id: int
    class_id: int
    item: str
 
class Tasks(BaseModel):
    task_id: int
    report_id: int
    start_time: str
    task_description: str
 
class Review(BaseModel):
    review_id: int
    report_id: int
    successes: str
    failures: str
    ai_comment: str
 
class GenAssessmentRequest(BaseModel):
    start_time: list[str]
    task_description: list[str]
    success: str
    failure: str
# レスポンスモデル
class GenAsseResponse(BaseModel):
    ef_plus_points: list[int]  # EF項目のIDのリスト
    ef_minus_points: list[int]  # マイナスEF項目のIDのリスト
    assessment: str  # AIからのアドバイス
   