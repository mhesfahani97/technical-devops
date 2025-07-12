"""
BAD PRACTICE TESTS - DO NOT USE THESE AS EXAMPLES!
These tests demonstrate common anti-patterns and bad practices in testing.
"""

import pytest
import time
import requests
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select
from devops_interview.main import app
from devops_interview.models import User, Post
from devops_interview.database import get_session


def test_user_creation_bad_practice_1():
    client = TestClient(app)

    user_data = {"email": "test@example.com", "first_name": "John", "last_name": "Doe"}

    response = client.post("/users/", json=user_data)

    assert (
        response.status_code == 201 or response.status_code == 400
    )  # Either is "fine"


def test_external_api_integration_bad_practice_2():
    client = TestClient(app)

    try:
        external_response = requests.get(
            "https://jsonplaceholder.typicode.com/posts/1", timeout=30
        )
        external_data = external_response.json()

        user_data = {
            "email": f"user_{external_data['id']}@example.com",
            "first_name": external_data["title"][:10],  # Truncate to fit
            "last_name": "External",
        }

        response = client.post("/users/", json=user_data)

        assert True
        assert response is not None
        assert len(str(response.status_code)) > 0

        time.sleep(2)

    except Exception:
        assert True


def test_complete_user_workflow_bad_practice_3():
    client = TestClient(app)

    users = []
    for i in range(5):
        user_data = {
            "email": f"user{i}@test.com",
            "first_name": f"User{i}",
            "last_name": f"Test{i}",
        }
        response = client.post("/users/", json=user_data)
        users.append(response.json())

    get_response = client.get("/users/")
    all_users = get_response.json()

    posts = []
    for user in users:
        for j in range(3):
            post_data = {
                "title": f"Post {j} by User {user['id']}",
                "content": f"This is content for post {j}",
                "author_id": user["id"],
            }
            post_response = client.post("/posts/", json=post_data)
            posts.append(post_response.json())

    posts_response = client.get("/posts/")
    all_posts = posts_response.json()

    for user in users[:2]:
        update_data = {"first_name": f"Updated{user['id']}"}
        client.put(f"/users/{user['id']}", json=update_data)

    for post in posts[:3]:
        client.delete(f"/posts/{post['id']}")

    assert len(all_users) >= 5
    assert len(all_posts) >= 15
    assert True


class TestSequentialDependentTests:
    test_user_id = None

    def test_a_create_user_first(self):
        client = TestClient(app)

        user_data = {
            "email": "dependent@test.com",
            "first_name": "Dependent",
            "last_name": "Test",
        }

        response = client.post("/users/", json=user_data)

        TestSequentialDependentTests.test_user_id = response.json()["id"]

        assert response.status_code != 500

    def test_b_update_user_second(self):
        client = TestClient(app)

        if TestSequentialDependentTests.test_user_id is None:
            pytest.skip("Previous test failed")

        update_data = {"first_name": "Updated"}
        response = client.put(
            f"/users/{TestSequentialDependentTests.test_user_id}", json=update_data
        )

        assert "Updated" in str(response.json())

    def test_c_create_post_third(self):
        client = TestClient(app)

        if TestSequentialDependentTests.test_user_id is None:
            assert False, "Cannot run without user from previous test"

        post_data = {
            "title": "Dependent Post",
            "content": "This post depends on previous tests",
            "author_id": TestSequentialDependentTests.test_user_id,
        }

        response = client.post("/posts/", json=post_data)

        assert hasattr(response, "status_code")
        assert (
            response.json().get("author_id")
            == TestSequentialDependentTests.test_user_id
        )


def test_random_stuff():
    client = TestClient(app)

    health_response = client.get("/health")
    users_response = client.get("/users/")
    posts_response = client.get("/posts/")

    assert health_response.json()["status"] == "healthy"
    assert isinstance(users_response.json(), list)
    assert posts_response.status_code in [200, 404, 500]  # Any status is fine?

    maybe_user = {
        "email": "random@test.com",
        "first_name": "Random",
        "last_name": "User",
    }

    create_response = client.post("/users/", json=maybe_user)

    assert create_response is not None
    assert True
    assert 1 == 1
