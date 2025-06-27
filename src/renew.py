from fastapi import FastAPI ,Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_connect import get_db  # DBセッション取得関数
from models import User ,UserUpdateRequest # Userモデル
 
 
app = FastAPI()
 
 
 
# class UserUpdateRequest(BaseModel):
#     class_id: int
#     period: int
#     ef_item_id_1: int
#     ef_item_id_2: int
#     ef_item_id_3: int
#     ef_item_id_4: int
#     ef_item_id_5: int
   
 
 
@app.put("/user/update/{user_id}", response_model=dict)
def update_user_profile(user_id: str, request: UserUpdateRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.class_id = request.class_id
    db_user.period = request.period
    db_user.ef_item_id_1 = request.ef_item_id_1
    db_user.ef_item_id_2 = request.ef_item_id_2
    db_user.ef_item_id_3 = request.ef_item_id_3
    db_user.ef_item_id_4 = request.ef_item_id_4
    db_user.ef_item_id_5 = request.ef_item_id_5
    db.commit()
    db.refresh(db_user)
    return {"message": "User profile updated"}
 