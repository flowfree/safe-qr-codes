#!/usr/bin/env python 

from datetime import datetime
import uuid
import shutil
import os

from fastapi import FastAPI, UploadFile, HTTPException
import puremagic


app = FastAPI()


@app.get('/')
def home():
    return {
        'message': 'API is up and running. xxx',
        'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }


def read_pdf(filename):
    return {'message': 'PDF file processed'}


def read_docx(filename):
    return {'message': 'DOCX file processed'}


def read_image(filename):
    return {'message': 'Image file processed'}


@app.post('/upload_file')
async def upload_file(file: UploadFile):
    try:
        file_type = puremagic.from_stream(file.file, mime=True)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail='Error determining file type.'
        )

    try:
        fileext = os.path.splitext(file.filename)[1]
        filename = f'/tmp/{uuid.uuid4()}{fileext}'

        with open(filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        supported_types = {
            "application/pdf": read_pdf,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": read_docx,
            "image/jpeg": read_image,
            "image/png": read_image,
        }

        if file_type in supported_types:
            return supported_types[file_type](filename)
        else:
            raise HTTPException(
                status_code=400, 
                detail='Unsupported file type'
            )

    finally:
        os.remove(filename)
