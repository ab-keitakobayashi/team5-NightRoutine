from fastapi import APIRouter, Depends, HTTPException, Query
from renew import UserUpdateRequest
from sqlalchemy.orm import Session
from typing import List
from models import (
    User,
    ReportsModel,
    UserResiRequest,
    UserResiResponse,
    Report,
    UserUpdateRequest
)

from db_connect import get_db

router = APIRouter()

@router.put("/user/update/{user_id}", response_model=dict)
def update_user_profile(user_id: str, request: UserUpdateRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.class_id = request.class_id
    user.period = request.period
    user.ef_item_id_1 = request.ef_item_id_1
    user.ef_item_id_2 = request.ef_item_id_2
    user.ef_item_id_3 = request.ef_item_id_3
    user.ef_item_id_4 = request.ef_item_id_4
    user.ef_item_id_5 = request.ef_item_id_5
    db.commit()
    return {"message": "User profile updated"}