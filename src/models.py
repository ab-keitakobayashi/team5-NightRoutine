from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
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

class ReportsModel(Base):
    __tablename__ = "reports"

    user_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, primary_key=True, index=True)
    write_date = Column(DateTime, default=datetime, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)  # 0: 未削除, 1: 削除済み   

class tasksModel(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, primary_key=True, index=True)
    startTime = Column(DateTime, nullable=False)
    tasks_description = Column(String, nullable=False)


class ReviewsModel(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, primary_key=True, index=True)
    successes = Column(String, nullable=False)
    failures = Column(String, nullable=False)
    ai_comment = Column(String, nullable=False)

# Pydanticモデル
# データのバリデーションとシリアライズを行うためのモデル]

# Post


class UserUpdateRequest(BaseModel):
    user_id: int
    class_id: int
    period: int
    efitem_id: int




class Report(BaseModel):

    report_id: int
    startTime : str
    endTime : str
    successes: str
    failures : str
    tasks : str


class ReportResponse(BaseModel):

    user_id: int
    report_id: int
    startTime : str
    endTime : str
    successes: str
    failures : str
    tasks : str

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
