import sys
import os
import pytest
from fastapi.testclient import TestClient

# Arrange: FastAPIアプリのインポート
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app

client = TestClient(app)

def test_root_redirects_to_static_index():
    # Arrange: テストクライアントは上で準備済み
    # Act: ルートエンドポイントにGETリクエスト（リダイレクトを追跡しない）
    response = client.get("/", follow_redirects=False)
    # Assert: 302リダイレクトで/static/index.htmlに飛ぶこと
    assert response.status_code == 307 or response.status_code == 302
    assert response.headers["location"].endswith("/static/index.html")

def test_activities_returns_all_activities():
    # Arrange: テストクライアントは上で準備済み
    # Act: /activitiesエンドポイントにGETリクエスト
    response = client.get("/activities")
    # Assert: ステータスコードとレスポンス内容を検証
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# 他のエンドポイントがあれば同様にAAAパターンでテストを追加してください。
