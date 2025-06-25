from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models import (
    PostCreate,
    PostResponse,
    Post,
    TaglineRequest,
    UserCreate,
    UserResponse,
    LikeCreate,
    LikeResponse,
    PostWithLikeInfo,
)

from db import get_db
from bedrock import call_bedrock

router = APIRouter()