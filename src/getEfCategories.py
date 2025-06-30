from fastapi import  HTTPException,FastAPI, Depends
from sqlalchemy.orm import Session, joinedload
from db_connect import get_db
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

app = FastAPI()

Base = declarative_base()

class EfItemsModel(Base):
    __tablename__ = "ef_items"

    ef_item_id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    ef_category_id = Column(Integer, nullable=False)


class EfCategoriesModel(Base):
    __tablename__ = "ef_categories"

    ef_category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)
    parent_category_id = Column(Integer, nullable=True)

class EfCategoryResponse(BaseModel):
    parentcategoryname: str
    categoryname: str
    item: str

@app.get("/efitems/{ef_item_id}", response_model=EfCategoryResponse)
def get_efitem_with_categories(ef_item_id: int, db: Session = Depends(get_db)):
    # efitemsを取得
    efitem = db.query(EfItemsModel).filter(EfItemsModel.ef_item_id == ef_item_id).first()
    if not efitem:
        raise HTTPException(status_code=404, detail="efitem not found")

    # カテゴリを取得
    category = db.query(EfCategoriesModel).filter(EfCategoriesModel.ef_category_id == efitem.ef_category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="category not found")

    # 親カテゴリを取得
    parent_category = None
    if category.parent_category_id is not None:
        parent = db.query(EfCategoriesModel).filter(EfCategoriesModel.ef_category_id == category.parent_category_id).first()
        parent_category_name = parent.category_name if parent else None
    else:
        parent_category_name = None
    # レスポンスを作成
    response = EfCategoryResponse(
        parentcategoryname=parent_category_name,
        categoryname=category.category_name,
        item=efitem.item
    )

    return response