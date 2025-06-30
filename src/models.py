from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional
# """
# DB接続設定とモデル定義
# """
# # DB接続設定
# DATABASE_URL = "mysql+pymysql://admin:fy26admin@fy26-training-handson-db.cxok2mc8wgeq.ap-northeast-1.rds.amazonaws.com:3306/handson" ##URL
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# DBモデル定義
# データベースのテーブルを定義するためのモデルクラスを作成します。

# Userモデル
# ユーザーテーブルを定義します。
class User(Base):
    __tablename__ = "testusers"

    user_id = Column(String, primary_key=True, index=True)
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

# Tasksモデル
# タスクテーブルを定義します。
class TasksModel(Base):
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
# Reviewsモデル
# レビューのテーブルを定義します。
class ReviewsModel(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, unique= True,nullable=True)#
    successes = Column(String, nullable=False)
    failures = Column(String, nullable=False)
    ai_comment = Column(String, nullable=False)

# Reportsモデル
# レポートのテーブルを定義します。
class ReportsModel(Base):
    __tablename__ = "reports"

    user_id = Column(String, unique= True,nullable=True)#ForeignKey('testusers.user_id'))
    report_id = Column(Integer, primary_key=True, index=False)
    write_date = Column(DateTime, default=datetime, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)  # 0: 未削除, 1: 削除済み

# Scoresモデル
# スコアのテーブルを定義します。
class ScoresModel(Base):
    __tablename__ = "scores"
    score_id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer, nullable=False)
    ef_item_id = Column(Integer, nullable=False)
    report_id = Column(Integer, nullable=False)

 # EFモデル
# EF項目のテーブルを定義します。
class EfModel(Base):
    __tablename__ = "ef_items" # テーブル名
    ef_item_id = Column(Integer, primary_key=True) # 主キー
    ef_category_id = Column(Integer, nullable=False) # カテゴリID
    class_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False) # アイテム名
    
# EFカテゴリモデル
# EF項目のカテゴリを定義します。
class EfItemsModel(Base):
    __tablename__ = "ef_items"

    ef_item_id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    ef_category_id = Column(Integer, nullable=False)

# EFカテゴリモデル
# EF項目のカテゴリを定義します。
class EfCategoriesModel(Base):
    __tablename__ = "ef_categories"

    ef_category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)
    parent_category_id = Column(Integer, nullable=True)


# Pydanticモデル
# データのバリデーションとシリアライズを行うためのモデル]

# Post

# UserRequestモデル
class UserRequest(BaseModel):
    user_name: str
    user_mailAddress: str
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
    
# Reportモデル
# レポートのデータを定義します。
class Report(BaseModel):
    start_time: List[str]
    # endTime: List[str]
    successes: str
    failures: str
    tasks: List[str] 

# ReportResponseモデル
# レポートのレスポンスデータを定義します。
class ReportResponse(BaseModel):
    
    start_time: List[str]  # タスクの開始時間のリスト
    successes: str  # 成功したタスクの説明
    failures: str  # 失敗したタスクの説明
    tasks: List[str]  # タスクの説明
    assessment: dict

# ReportRegiResponseモデル  
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

# UserUpdateRequestモデル
# ユーザープロフィールの更新リクエストデータを定義
class UserUpdateRequest(BaseModel):
    user_name: str
    class_id: int
    period: int
    ef_item_id_1: int
    ef_item_id_2: int
    ef_item_id_3: int
    ef_item_id_4: int
    ef_item_id_5: int


# UserResiRequestモデル
# ユーザー登録リクエストデータを定義します。
class UserResiRequest(BaseModel):
    name: str
    class_id: int
    period: int
    ef_item_id_array: list[int]  # Changed to a list for flexibility

# UserResiResponseモデル
# ユーザー登録レスポンスデータを定義します。
class UserResiResponse(BaseModel):
    user_id: str
    name: str
    class_id: int
    period: int
    avatar_id: int
    enemy_id: int
    enemy_hp: int
    ef_item_id_1: Optional[int]
    ef_item_id_2: Optional[int]
    ef_item_id_3: Optional[int]
    ef_item_id_4: Optional[int]
    ef_item_id_5: Optional[int]




# EF_Itemsモデル
# EF項目のデータを定義します。
class Ef_Items(BaseModel):
    ef_item_id: int
    ef_category_id: int
    class_id: int
    item: str
 
# Tasksモデル
# タスクのデータを定義します。
class Tasks(BaseModel):
    task_id: int
    report_id: int
    start_time: str
    task_description: str
 
 
# Reviewsモデル
# レビューのデータを定義します。
class Review(BaseModel):
    review_id: int
    report_id: int
    successes: str
    failures: str
    ai_comment: str

#GenAssessmentRequestモデル
# AIによるEF評価リクエストデータを定義します。
class GenAssessmentRequest(BaseModel):
    start_time: list[str]
    task_description: list[str]
    success: str
    failure: str
    
# GenAsseResponseモデル
# AIによるEF評価レスポンスデータを定義します。
class GenAsseResponse(BaseModel):
    ef_plus_points: list[int]  # EF項目のIDのリスト
    ef_minus_points: list[int]  # マイナスEF項目のIDのリスト
    assessment: str  # AIからのアドバイス
   
# SummaryRequestモデル
# レビューとアドバイスの集計リクエストデータを定
class SummaryRequest(BaseModel):
    start_date: datetime
    end_date: datetime

# EF_Itemsデータモデル
# EF項目のデータを定義します。
class ef_items_data(BaseModel):
    ef_item_id: int
    item: str

# ReviewsAICommentデータモデル
# レビューのAIコメントデータを定義します。
class reviews_aicomment_data(BaseModel):
    ai_comment: str
    
# EFアセスメントサマリーモデル
# EF項目ごとのアセスメントサマリーを定義します。
class EfAssessmentSummary(BaseModel):
    ef_item_id: int
    total_score: int
    
# EFスコアサマリーモデル
# EF項目ごとのスコアサマリーを定義します。
class EfScoreSummary(BaseModel):
    ef_item_id: int
    total_score: int
    dates: List[str]
    

# EFカテゴリレスポンスモデル
# EFカテゴリのレスポンスデータを定義します。
class EfCategoryResponse(BaseModel):
    parentcategoryname: str
    categoryname: str
    item: str