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


def test_signup_and_remove_signup_for_activity():
    # Arrange
    test_email = "testuser@example.com"
    activity = "Chess Club"

    # Act: まずPOSTで参加登録
    response_signup = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert: 登録成功
    print("DEBUG response_signup.text:", repr(response_signup.text))
    assert response_signup.status_code == 200
    assert response_signup.json()["message"].startswith("Signed up")

    # Act: DELETEで登録削除
    response_delete = client.delete(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert: 削除成功
    assert response_delete.status_code == 200
    assert response_delete.json()["message"].startswith("Removed")

    # Act: もう一度削除（存在しない場合）
    response_delete2 = client.delete(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert: 404エラー
    assert response_delete2.status_code == 404

# 他のエンドポイントがあれば同様にAAAパターンでテストを追加してください。
