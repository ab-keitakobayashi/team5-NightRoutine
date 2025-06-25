from fastapi import APIRouter, Depends, HTTPException, Query
from renew import UserUpdateRequest
from sqlalchemy.orm import Session
from typing import List
from models import (
    User,  
    Reports,
    UserUpdateRequest,
    UserResiRequest,
    UserResiResponse
)

from db_connect import get_db

router = APIRouter()

@router.put("/user/update/{user_id}", response_model=dict)
def update_user_profile(user_id: int, request: UserUpdateRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.class_id = request.class_id
    user.period = request.period
    user.efitem_id = request.efitem_id
    db.commit()
    return {"message": "User profile updated"}

@router.post("/user/regi", response_model=UserResiResponse)
def create_item(user: UserResiRequest, db_session: Session = Depends(get_db)):
    db_user = User(
        user_name=user.name,
        user_mailAddress=user.mailAddress,
        class_id=user.class_id,
        period=user.period,
        avatar_id=1,
        enemy_id=1,
        enemy_hp=100,
        ef_item_id1=user.ef_item_id1,
        ef_item_id2=user.ef_item_id2,
        ef_item_id3=user.ef_item_id3,
        ef_item_id4=user.ef_item_id4,
        ef_item_id5=user.ef_item_id5
    )
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
        ef_item_id1=db_user.ef_item_id1,
        ef_item_id2=db_user.ef_item_id2,
        ef_item_id3=db_user.ef_item_id3,
        ef_item_id4=db_user.ef_item_id4,
        ef_item_id5=db_user.ef_item_id5
    )