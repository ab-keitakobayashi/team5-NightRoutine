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
    ef_item_id1 = Column(Integer, nullable=False)
    ef_item_id2 = Column(Integer, nullable=False)
    ef_item_id3 = Column(Integer, nullable=False)
    ef_item_id4 = Column(Integer, nullable=False)
    ef_item_id5 = Column(Integer, nullable=False)

class Reports(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)
    startTime = Column(String, nullable=False)
    endTime = Column(String, nullable=False)
    successes = Column(String, nullable=False)
    failures = Column(String, nullable=False)
    tasks = Column(String, nullable=False)



# Pydanticモデル
# データのバリデーションとシリアライズを行うためのモデル]


# Post


class UserUpdateRequest(BaseModel):
    user_id: int
    class_id: int
    period: int
    efitem_id: int