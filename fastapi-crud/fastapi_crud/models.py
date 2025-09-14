from sqlalchemy import Column, Integer, String
from .database import Base  # 同じディレクトリにある database.py から Base を読み込む


class Item(Base):
    __tablename__ = "items"  # DB上のテーブル名

    id = Column(Integer, primary_key=True, index=True)  # 主キー
    name = Column(String, index=True)  # 名前
    description = Column(String, index=True)  # 説明
