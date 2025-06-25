from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_connect import get_db  # DBセッション取得関数
from models import User  # Userモデル

app = FastAPI()

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


@app.get("/user/{user_id}", response_model=UserResiResponse)
def get_user(user_id: int, db_session: Session = Depends(get_db)):
    """
    ユーザー情報を取得するエンドポイント
    :param user_id: ユーザーID
    :param db_session: データベースセッション
    :return: ユーザー情報
    """
    #try:
    db_user = db_session.query(User).filter(User.user_id == user_id).first()
    # except Exception as e:
    #     return {"error": "usernot found", "details": str(e)}
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