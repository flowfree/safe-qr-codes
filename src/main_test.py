import os
import pytest
from fastapi.testclient import TestClient
from .main import app


# Create a TestClient instance to send requests to the FastAPI app
client = TestClient(app)


# Define a fixture to clean up uploaded files after testing
@pytest.fixture(scope="module")
def cleanup_uploaded_files():
    yield
    # Clean up files in the "/tmp" directory after testing
    for filename in os.listdir("/tmp"):
        if filename.startswith("test_"):
            file_path = os.path.join("/tmp", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


# Create a sample image file in the temporary directory
def create_sample_image_file():
    image_data = b'\x89PNG\r\n\x1a\n...'
    with open("/tmp/test_image.png", "wb") as f:
        f.write(image_data)


def test_upload_file_no_file():
    response = client.post("/upload_file/")
    assert response.status_code == 422


def test_upload_file_with_file(cleanup_uploaded_files):
    create_sample_image_file()

    with open("/tmp/test_image.png", "rb") as image_file:
        files = {"file": ("test_image.png", image_file)}
        response = client.post("/upload_file", files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Image file processed"}
