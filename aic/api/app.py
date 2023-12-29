import logging
import os
import random

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from psycopg2 import OperationalError, ProgrammingError

<<<<<<< HEAD
from aic.db.main import DataBase
=======
from aic.api.utilities import create_connection, is_valid_image
from aic.clsf_model.onnx_inference import Inference
>>>>>>> 28ecc83 (add classification model)

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

    db = DataBase(db_name, db_user, db_password, db_host, db_port)
    try:
        with db.connection.cursor():
            return PlainTextResponse(
                content="Successfully connected to db", status_code=200
            )

    except (OperationalError, ProgrammingError) as e:
        logging.warning(f"""The error '{e}' occurred""")
        raise HTTPException(status_code=400) from e

    finally:
        db.connection.close()


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

    contents = await file.read()
    arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        return PlainTextResponse(content="Image is invalid", status_code=400)

    db = DataBase(db_name, db_user, db_password, db_host, db_port)
    db.create_table()

    image_hash = hash(image.tostring())
    hit = db.find_picture_in_table(image_hash)
    if not hit:
        print("No image with same hash in db, running the model")
        model = Inference()
        label = model()
        db.insert_label_into_table(image_hash, label)
    else:
        print("Found image with same hash in db, getting the label")
        label = hit

    return JSONResponse(
        content={
            "image_name": file.filename,
            "image_hash": image_hash,
            "label": label,
        },
        status_code=200,
    )

