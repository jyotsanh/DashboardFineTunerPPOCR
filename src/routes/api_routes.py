import io

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile
from PyPDF2 import PdfReader

from _models import _get_ocr_model, _release_ocr_model

router = APIRouter()

MAX_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_PAGES = 10


@router.post("/upload-pdf", tags=["PDF File Upload"])
async def upload_pdf_file(Ufile: UploadFile):
    """Upload a PDF file and return its metadata.

    Args:
        Ufile (UploadFile): The file to be uploaded.
    Returns:
        dict: Metadata of the uploaded file, including:
          - filename
          - content type.
    """
    try:
        if (
            Ufile.content_type != "application/pdf" or Ufile.size > MAX_SIZE
        ):  # Check if the file is a PDF and within size limits
            return HTTPException(
                status_code=400,
                detail="""
                Invalid file type.
                Only PDF files are allowed and size must be less than 10 MB.
                """,
            )
        content = await Ufile.read()
        reader = PdfReader(io.BytesIO(content))
        if len(reader.pages) > MAX_PAGES:
            return HTTPException(
                status_code=400,
                detail="PDF file exceeds the maximum allowed pages (10).",
            )
        data = {
            "filename": Ufile.filename,
            "content_type": Ufile.content_type,
        }
        return data
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/upload-image", tags=["Single File Upload"])
async def upload_image_file(UImage: UploadFile):
    """Upload an image file and return its metadata.

    Args:
        Ufile (UploadFile): The file to be uploaded.
    Returns:
        dict: Metadata of the uploaded file, including:
          - filename
          - content type.
    """
    try:
        if (
            UImage.content_type not in ["image/jpeg", "image/png"]
            or UImage.size > MAX_SIZE
        ):  # Check if the file is an image and within size limits
            return HTTPException(
                status_code=400,
                detail="""
                Invalid file type.
                Only JPEG and PNG images are allowed and
                size must be less than 10 MB.
                """,
            )
        ocr_model = _get_ocr_model()
        image_content = await UImage.read()
        nparr = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        ocr_results = ocr_model.predict(image)
        # print(ocr_results[0]["rec_scores"])
        ocr_res = {}
        accuracy_list = ocr_results[0]["rec_scores"]
        rec_word_list = ocr_results[0]["rec_texts"]
        for index in range(len(accuracy_list)):
            ocr_res[rec_word_list[index]] = accuracy_list[index]
        data = {
            "filename": UImage.filename,
            "content_type": UImage.content_type,
            "results": ocr_res,
        }
        return data
    except Exception as e:
        _release_ocr_model()
        return HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/image_orientation", tags=["Image Orientation"])
async def orienation_image(Ufile: UploadFile):
    try:
        pass
    except RuntimeError as e:
        return HTTPException(
            status_code=500,
            detail=f"Error loading OCR model: {str(e)}",
        )
