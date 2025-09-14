# スキーマの一般的な意味
# データベーススキーマ
# DBの構造定義（テーブル・カラム・制約など）
# 例: PostgreSQLの schema（publicスキーマなど）
# データ構造のひな型
# JSON Schema とか XML Schema のように、「データがこの形で来るよ」という設計図
# APIの世界ではこちらの意味でよく使う

from pydantic import BaseModel


# 共通部分
class ItemBase(BaseModel):
    name: str
    description: str | None = None  # 説明は省略可


# 新規作成リクエスト用
class ItemCreate(ItemBase):
    pass  # ItemBase と同じなのでそのまま継承


# レスポンス用（DBから返す時に id が必要）
class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True  # SQLAlchemyモデルを直接返せるようにする
