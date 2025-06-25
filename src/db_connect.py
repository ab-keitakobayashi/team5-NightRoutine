from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv
import os

# ローカル開発時のみ .env を読み込む
load_dotenv()

# 環境変数からDB URLを取得
database_url = "mysql+pymysql://admin:fy26admin@aws-handson-db-group-5.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com/NightRoutine"

# エンジンを作成
engine = create_engine(database_url)

# セッションを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースを初期化（Lambda本番では別管理の方がよいが、簡易化のため残す）
Base.metadata.create_all(bind=engine)


# データベースセッションを取得する依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
