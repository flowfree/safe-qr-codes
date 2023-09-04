from typing import List, Dict
from zipfile import ZipFile
from io  import BytesIO
import base64

from PIL import Image
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode


def read_docx(docx_path: str):
    images = []
    with ZipFile(docx_path, 'r') as zip:
        for filename in zip.namelist():
            if filename.startswith('word/media/') and \
                any(filename.endswith(ext) for ext in ['.jpeg', '.jpg', '.png', '.gif']):
                with zip.open(filename) as image_file:
                    img = Image.open(BytesIO(image_file.read()))
                    images.append(img)
    return decode_qr_codes(images)


def read_pdf(pdf_path: str):
    images = []
    pages = convert_from_path(pdf_path)
    for page in pages:
        images.append(page)
    return decode_qr_codes(images)


def read_image(filename: str):
    with Image.open(filename) as img:
        return decode_qr_codes([img])


def decode_qr_codes(images: List[Image.Image]) -> List[Dict[str, str]]:
    result = []

    for img in images:
        # Convert the PIL image to bytes
        buffered = BytesIO()
        img.save(buffered, format='PNG')
        img_bytes = buffered.getvalue()

        # Decode QR codes in the image
        decoded_objects = decode(Image.open(BytesIO(img_bytes)))

        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            
            # Extract the bounding box coordinates of the QR code
            x, y, w, h = obj.rect
            subimg = img.crop((x, y, x + w, y + h))

            # Encode the QR code image as base64
            buffered = BytesIO()
            subimg.save(buffered, format='PNG')
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Append the data and QR code image to the result list
            result.append({
                'data': data, 
                'image': encoded_image
            })

    return result
