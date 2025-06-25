from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models import (
    User,  
    ItemModel,
    Reports 
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