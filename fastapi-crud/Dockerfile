# ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /app

# 依存ライブラリをコピー＆インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリをコピー
COPY . .

# コンテナ起動時に実行するコマンド
CMD ["uvicorn", "fastapi_crud.main:app", "--host", "0.0.0.0", "--port", "8000"]
