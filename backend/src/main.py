#!/usr/bin/env python 

from datetime import datetime
import uuid
import shutil
import io
import os

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from dotenv import load_dotenv
import puremagic

from .qrcodes import read_pdf, read_docx, read_image
from .safe_urls import check_url


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


app = FastAPI()

origins = [
    'http://localhost:3000',
    'https://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/')
def home():
    return {
        'message': 'API is up and running.',
        'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }


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

        functions = {
            "application/pdf": read_pdf,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": read_docx,
            "image/jpeg": read_image,
            "image/png": read_image,
        }

        if file_type in functions:
            qr_codes = functions[file_type](filename)
        else:
            raise HTTPException(
                status_code=400, 
                detail='Unsupported file type'
            )

    finally:
        os.remove(filename)

    for qr_code in qr_codes:
        if qr_code['data'].startswith('http'):
            is_safe, threat_details = check_url(qr_code['data'], GOOGLE_API_KEY)
        else:
            is_safe, threat_details = True, []
        
        qr_code['isSafe'] = is_safe
        qr_code['threatDetails'] = threat_details

    return qr_codes
