import json

import requests
from pymongo import MongoClient
import pytest


@pytest.fixture(scope='module')
def db():
    client = MongoClient("mongodb://localhost:27017/cashcog")
    db = client.expenses_db
    return db


def test_query_api(db):
    r = requests.get("http://127.0.0.1:5000/query")
    response_payload = r.json()
    assert len(response_payload['data']) > 0
    assert r.status_code == 200


def test_query_api_with_parameters(db):
    data = db.expenses.find_one({"status": {"$exists": False}})
    url = "http://127.0.0.1:5000/query?first_name={}&last_name={}&amount={}&currency={}".format(
        data["employee"]["first_name"],
        data["employee"]["last_name"],
        data["amount"],
        data["currency"]
    )
    r = requests.get(url)
    response_payload = r.json()
    assert r.status_code == 200
    assert response_payload["data"][0]["first_name"] == data["employee"]["first_name"]
    assert response_payload["data"][0]["last_name"] == data["employee"]["last_name"]
    assert response_payload["data"][0]["amount"] == data["amount"]
    assert response_payload["data"][0]["currency"] == data["currency"]


def test_query_api_with_invalid_parameters(db):
    data = db.expenses.find_one({"status": {"$exists": False}})
    url = "http://127.0.0.1:5000/query?first_name={}&last_name={}&amount={}&currency={}".format(
        data["employee"]["first_name"],
        data["employee"]["last_name"],
        data["amount"],
        data["currency"]
    )
    r = requests.get(url)
    response_payload = r.json()
    assert r.status_code == 200
    assert response_payload["data"][0]["first_name"] == data["employee"]["first_name"]
    assert response_payload["data"][0]["last_name"] == data["employee"]["last_name"]
    assert response_payload["data"][0]["amount"] == data["amount"]
    assert response_payload["data"][0]["currency"] == data["currency"]


def test_validate_api(db):
    data = db.expenses.find_one({"status": {"$exists": False}}, {"uuid": 1})
    url = "http://127.0.0.1:5000/validate/"
    data = {
        "uuid": data["uuid"],
        "status": "approve"
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    response_payload = r.json()
    assert r.status_code == 200
    assert response_payload["success"] is True
    assert response_payload["status"] == "approve"


def test_validate_api_invalid_payload(db):
    url = "http://127.0.0.1:5000/validate/"
    data = {
        "uuid": "yolo",
        "status": "approve"
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    response_payload = r.json()
    assert r.status_code == 400
    assert "errors" in response_payload
