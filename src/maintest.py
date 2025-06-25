from fastapi import FastAPI
from routers import router
from db_connect import engine
from models import Base
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os

ROOT_PATH = os.environ.get("FASTAPI_ROOT_PATH", "")

app = FastAPI(root_path=ROOT_PATH)

DEV_ORIGIN = os.environ.get("FRONT_DEV_ORIGIN", "http://localhost:5173")
PROD_ORIGIN = os.environ.get("FRONT_PROD_ORIGIN", "")

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=[DEV_ORIGIN, PROD_ORIGIN],  # 必要に応じて特定のオリジンに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(router)

# データベースを初期化
Base.metadata.create_all(bind=engine)

# AWS Lambdaでのデプロイ用
handler = Mangum(app)


# 疎通確認用エンドポイント
@app.get("/")
async def root():
    return {"message": "Hello World"}
