from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..db import get_db  # DBセッション取得関数
from ..models import User  # Userモデル

router = APIRouter()


class UserUpdateRequest(BaseModel):
    user_id: int
    class_id: int
    period: int
    efitem_id: int

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