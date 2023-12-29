import pytest
from fastapi.testclient import TestClient

from aic.api.app import app
from pathlib import Path

VALID_IMAGE_PATH = "tests/test_local/test_api/files/valid_img.png"
INVALID_IMAGE_PATH = "tests/test_local/test_api/files/invalid_img.png"

client = TestClient(app)


@pytest.fixture
def test_image_valid():
    image_path = Path(VALID_IMAGE_PATH)
    return image_path


@pytest.fixture
def test_image_invalid():
    image_path = Path(INVALID_IMAGE_PATH)
    return image_path


def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_upload_image_and_classify_invalid_file(test_image_invalid):
    with test_image_invalid.open("rb") as image_file:
        files = {"file": ("invalid_img.png", image_file, "image/png")}
        response = client.post("/upload", files=files)

    assert response.status_code == 400
    assert response.content == b"Image is invalid"


def test_upload_image_and_classify_no_file():
    response = client.post("/upload")
    assert response.status_code == 400
    assert response.content == b"No upload file sent"
