from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel,Base
from db_connect import get_db  # DBセッション取得関数



# DBモデル定義
class efInfo(Base):
    __tablename__ = "ef_items" # テーブル名
    ef_item_id = Column(Integer, primary_key=True) # 主キー
    ef_category_id = Column(Integer, nullable=False) # カテゴリID
    class_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False) # アイテム名



# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# ①Itemテーブルを全件取得（サンプル実装済み）
@app.get("/items", response_model=ItemsResponse)
def get_items(db_session: Session = Depends(get_db_session)):
    items = db_session.query(ItemModel).all()
    # ItemModelのインスタンスをItemSchemaに変換
    items = [ItemResponse(id=item.id, name=item.name, price=item.price) for item in items]
    return ItemsResponse(items=items)

# ②idを指定してItemテーブルからデータ取得（サンプル実装済み）
@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db_session: Session = Depends(get_db_session)):
    item = db_session.query(ItemModel).filter(ItemModel.id == item_id).first()
    # itemが見つからない場合は404エラーを返す
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(id=item.id, name=item.name, price=item.price)

# ③nameを指定してItemテーブルからデータ取得（要実装）
@app.get("/items/by_name/{name}", response_model=ItemsResponse)
def get_items_by_name(name: str, db_session: Session = Depends(get_db_session)):
    items = db_session.query(ItemModel).filter(ItemModel.name == name).all()
    items = [ItemResponse(id=item.id, name=item.name, price=item.price) for item in items]
    return ItemsResponse(items=items)


# ④itemを追加（サンプル実装済み）
@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemRequest, db_session: Session = Depends(get_db_session)):
    db_item = ItemModel(name=item.name, price=item.price) # idは自動採番されるため、リクエストには含めない
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return ItemResponse(id=db_item.id, name=db_item.name, price=db_item.price)

# ⑤itemを更新（要実装）
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemRequest, db_session: Session = Depends(get_db_session)):
    db_item = db_session.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.price = item.price
    db_session.commit()
    db_session.refresh(db_item)
    return ItemResponse(id=db_item.id, name=db_item.name, price=db_item.price)


# ⑥itemを削除（要実装）
@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db_session: Session = Depends(get_db_session)):
    db_item = db_session.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_session.delete(db_item)
    db_session.commit()
    return ItemResponse(id=db_item.id, name=db_item.name, price=db_item.price)
