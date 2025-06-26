from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_connect import get_db  # DBセッション取得関数
from models import User, UserResiResponse, UserResiRequest  # Userモデル

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/users"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# class UserResiRequest(BaseModel):
#     name: str
#     mailAddress: str
#     class_id: int
#     period: int
#     ef_item_id1: int
#     ef_item_id2: int
#     ef_item_id3: int
#     ef_item_id4: int
#     ef_item_id5: int

# class UserResiResponse(BaseModel):
#     id: int
#     name: str
#     mailAddress: str
#     class_id: int
#     period: int
#     avatar_id: int
#     enemy_id: int
#     enemy_hp: int
#     ef_item_id_1: int
#     ef_item_id_2: int
#     ef_item_id_3: int
#     ef_item_id_4: int
#     ef_item_id_5: int

class UserResiRequest(BaseModel):
    name: str
    class_id: int
    period: int
    ef_item_id_array: list[int]  # Changed to a list for flexibility


class UserResiResponse(BaseModel):
    id: int
    name: str
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

@app.post("/user/regi", response_model=UserResiResponse)
def create_item(user: UserResiRequest, db_session: Session = Depends(get_db)):
    db_user = User(
        user_name=user.name,
        user_mailAddress= "dammy3@Gmail.com",
        class_id=user.class_id,
        period=user.period,
        avatar_id=1,
        enemy_id=1,
        enemy_hp=100,
    )
    # ef_item_id_1 〜 ef_item_id_5 に ef_item_id_array の値を順に代入
    for i in range(1, 6):
        value = user.ef_item_id_array[i - 1] if len(user.ef_item_id_array) >= i else None
        setattr(db_user, f"ef_item_id_{i}", value)

    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
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