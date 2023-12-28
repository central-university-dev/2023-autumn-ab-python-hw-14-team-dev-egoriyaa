import pytest
from fastapi.testclient import TestClient

from src.api.app import app
from pathlib import Path

client = TestClient(app)


@pytest.fixture
def test_image():
    image_path = Path("tests/assets/psi.png")
    return image_path


def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


# TODO: change test in accordance with added model
def test_upload_image_and_classify(test_image):
    with test_image.open("rb") as image_file:
        files = {"file": ("test_image.png", image_file, "image/png")}
        response = client.post("/upload", files=files)

    assert response.status_code == 200
    assert response.json()["image_name"] == "test_image.png"
    assert response.json()["label"] == "TBD"


def test_upload_image_and_classify_no_file():
    response = client.post("/upload")
    assert response.status_code == 400
    assert response.json()["message"] == "No upload file sent"
