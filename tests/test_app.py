import sys
import os
import pytest
from fastapi.testclient import TestClient

# Arrange: FastAPIアプリのインポート
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app

client = TestClient(app)

def test_root():
    # Arrange: テストクライアントは上で準備済み
    # Act: ルートエンドポイントにGETリクエスト
    response = client.get("/")
    # Assert: ステータスコードとレスポンス内容を検証
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

# 他のエンドポイントがあれば同様にAAAパターンでテストを追加してください。
