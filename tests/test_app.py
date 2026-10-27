import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

client = app.test_client()


def test_health():
    assert client.get("/health").get_json()["status"] == "ok"


def test_predict_setosa():
    r = client.post("/predict", json={"sepal_length": 5.1, "sepal_width": 3.5,
                                      "petal_length": 1.4, "petal_width": 0.2})
    assert r.status_code == 200 and r.get_json()["species"] == "setosa"


def test_predict_bad_input():
    assert client.post("/predict", json={"sepal_length": "x"}).status_code == 400


def test_metrics():
    assert b"app_requests_total" in client.get("/metrics").data
