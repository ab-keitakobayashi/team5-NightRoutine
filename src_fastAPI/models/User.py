from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_mailAddress = Column(String, unique=True, nullable=False)
    class_id = Column(Integer, nullable=True)
    period = Column(Integer, nullable=True)
    abator_id = Column(Integer, nullable=True)
    enemy_id = Column(Integer, nullable=True)
    enemy_hp = Column(Integer, nullable=True)
    ef_item_id1 = Column(Integer, nullable=True)
    ef_item_id2 = Column(Integer, nullable=True)
    ef_item_id3 = Column(Integer, nullable=True)
    ef_item_id4 = Column(Integer, nullable=True)
    ef_item_id5 = Column(Integer, nullable=True)