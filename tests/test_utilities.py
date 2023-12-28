from fastapi import UploadFile

from src.api.utilities import is_valid_image
from pathlib import Path


def test_is_valid_image_valid_image():
    image_path = Path("tests/assets/psi.png")
    assert is_valid_image(image_path) is True


def test_is_valid_image_invalid_image(tmp_path):
    text_data = b"This is not an image."
    text_path = tmp_path / "invalid_image.txt"
    with text_path.open("wb") as f:
        f.write(text_data)

    with text_path.open("rb") as text_file:
        upload_file = UploadFile(file=text_file, filename="invalid_image.txt")
    assert is_valid_image(upload_file) is False


def test_is_valid_image_empty_file(tmp_path):
    empty_path = tmp_path / "empty_file.txt"
    with empty_path.open("wb"):
        pass

    with empty_path.open("rb") as empty_file:
        upload_file = UploadFile(file=empty_file, filename="empty_file.txt")
        assert is_valid_image(upload_file) is False


def test_is_valid_image_invalid_image_exception(tmp_path):
    invalid_path = tmp_path / "invalid_image_exception.jpg"
    with invalid_path.open("wb"):
        pass

    with invalid_path.open("rb") as invalid_file:
        upload_file = UploadFile(
            file=invalid_file, filename="invalid_image_exception.jpg"
        )
        assert is_valid_image(upload_file) is False
