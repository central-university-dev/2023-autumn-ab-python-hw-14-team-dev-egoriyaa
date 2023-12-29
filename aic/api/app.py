import logging
import os
import random
import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from psycopg2 import OperationalError, ProgrammingError

from .utilities import create_connection, is_valid_image

random.seed(42)

db_user = os.getenv("POSTGRES_USER", "temp")
db_password = os.getenv("POSTGRES_PASSWORD", "temp")
db_name = os.getenv("POSTGRES_DB", "db")
table_name = os.getenv("POSTGRES_TABLE", "table")
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", "7654"))

app = FastAPI()


@app.get("/check_db")
def check_connection_to_db():
    """Check db connectivity.

    Raises:
        HTTPException: some error happened

    Returns:
        PlainTextResponse | HTTPException
    """
    connection = create_connection(db_name, db_user, db_password, db_host, db_port)
    try:
        with connection.cursor():
            return PlainTextResponse(
                content="Successfully connected to db", status_code=200
            )

    except (OperationalError, ProgrammingError) as e:
        logging.warning(f"""The error '{e}' occurred""")
        raise HTTPException(status_code=400) from e

    finally:
        connection.close()


@app.get("/health")
def read_health():
    """Check service health.

    Returns:
        JSONResponse: OK response
    """
    return JSONResponse(content={"status": "OK"}, status_code=200)


@app.post("/upload")
async def upload_image_and_classify(file: UploadFile | None = None):
    """Upload image using POST request and classify it using the ML model.

    Args:
        file (UploadFile | None, optional): an image to upload. Defaults to None.

    Returns:
        PlainTextResponse | JSONResponse: response
    """
    if not file:
        return PlainTextResponse(content="No upload file sent", status_code=400)
    else:
        file_path = Path(f"./{file.filename}")
        # image = Image.open(io.BytesIO(file.file))
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if not is_valid_image(file_path):
            return PlainTextResponse(content="Image is invalid", status_code=400)

        # TODO: read image, send to model and get the label
        label = "TBD"

        return JSONResponse(
            content={"image_name": file.filename, "label": label}, status_code=200
        )
