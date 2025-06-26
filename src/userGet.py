from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_connect import get_db  # DBセッション取得関数
from models import User, UserResiResponse  # Userモデル

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 必要に応じて追加
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/user/{user_id}", response_model=UserResiResponse)
def get_user(user_id: int, db_session: Session = Depends(get_db)):
    """
    ユーザー情報を取得するエンドポイント
    :param user_id: ユーザーID
    :param db_session: データベースセッション
    :return: ユーザー情報
    """
    db_user = db_session.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResiResponse(
        id=db_user.user_id,
        name=db_user.user_name,
        mailAddress=db_user.user_mailAddress,
        class_id=db_user.class_id,
        period=db_user.period,
        avatar_id=db_user.avatar_id,
        enemy_id=db_user.enemy_id,
        enemy_hp=db_user.enemy_hp,
        ef_item_id_1=db_user.ef_item_id_1,
        ef_item_id_2=db_user.ef_item_id_2,
        ef_item_id_3=db_user.ef_item_id_3,
        ef_item_id_4=db_user.ef_item_id_4,
        ef_item_id_5=db_user.ef_item_id_5
    )