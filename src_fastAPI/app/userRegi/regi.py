from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
#from sqlalchemy.orm import Session
#from ...util.db_connect import get_db  # DBセッション取得関数
from ...util.models import User  # Userモデル

router = APIRouter()
app = FastAPI()

class UserResiRequest(BaseModel):
    id = int
    name = str
    mailAddress = str
    class_id = int
    period = int
    ef_item_id1 = int
    ef_item_id2 = int
    ef_item_id3 = int
    ef_item_id4 = int
    ef_item_id5 = int

class UserResiResponse(BaseModel):
    id: int
    name: str
    mailAddress: str
    class_id: int
    period: int
    avatar_id: int
    enemy_id: int
    enemy_hp: int
    ef_item_id1: int
    ef_item_id2: int
    ef_item_id3: int
    ef_item_id4: int
    ef_item_id5: int

# ④itemを追加（サンプル実装済み）
@router.post("/user/regi", response_model=UserResiResponse)
def create_item(user: UserResiRequest): #, db_session: Session = Depends(get_db) 2⃣
    db_user = User(user_name=user.name, user_mailAddress=user.mailAddress,
                   class_id=user.class_id, period=user.period, avatar_id=1, #アバターIDの初期値
                   enemy_id=1, enemy_hp=100, #敵のIDとHPの初期値（仮）
                   ef_item_id1=user.ef_item_id1, ef_item_id2=user.ef_item_id2,
                   ef_item_id3=user.ef_item_id3, ef_item_id4=user.ef_item_id4,
                   ef_item_id5=user.ef_item_id5
                   ) # idは自動採番されるため、リクエストには含めない
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return UserResiResponse(id=db_user.id, name=db_user.name, mailAddress=db_user.mailAddress,
                             class_id=db_user.class_id, period=db_user.period, avatar_id=db_user.avatar_id,
                             enemy_id=db_user.enemy_id, enemy_hp=db_user.enemy_hp,
                             ef_item_id1=db_user.ef_item_id1, ef_item_id2=db_user.ef_item_id2,
                             ef_item_id3=db_user.ef_item_id3, ef_item_id4=db_user.ef_item_id4,
                             ef_item_id5=db_user.ef_item_id5)