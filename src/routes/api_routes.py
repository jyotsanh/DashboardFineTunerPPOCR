import io
from typing import List

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, Query, UploadFile
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader

from _models import _get_ocr_model, _release_ocr_model

router = APIRouter()

MAX_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_PAGES = 80


@router.post("/upload-pdf", tags=["PDF File Upload"])
async def upload_pdf_file(
    Ufile: UploadFile,
    user_id: str,
    start_page: int = 0,
    pages_to_read_at_once: int = Query(
        1, ge=1, le=10, description="How many pages to process at once"
    ),
):
    """Upload a PDF file and return its metadata.

    Args:
        Ufile (UploadFile): The file to be uploaded.
        pages_to_read_at_once (int): Page number to process (1-based indexing).
        user_id (str): User identifier from authentication.
    Returns:
        dict: OCR results for the requested page range and PDF metadata.
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
        total_pages = len(reader.pages)
        if start_page > total_pages:
            return HTTPException(
                status_code=400,
                detail="""start page should be smaller,
                        than total length of pdf""",
            )
        if pages_to_read_at_once > total_pages:
            return HTTPException(
                status_code=400,
                detail="""pages to read at once should be smaller,
                            than total length of pdf""",
            )
        if total_pages > MAX_PAGES:
            return HTTPException(
                status_code=400,
                detail=f"""PDF file exceeds the maximum allowed page
                         only upto ({MAX_PAGES}) pages are allowed.""",
            )
        images = convert_from_bytes(content)
        _ocr_model = _get_ocr_model()
        data = {}
        idx = 0
        for i, img in enumerate(images):
            if i + 1 >= start_page:
                if idx == pages_to_read_at_once:
                    break
                ocr_res = _ocr_model.predict(np.array(img))
                temp = {}
                accuracy_list = ocr_res[0]["rec_scores"]
                rec_word_list = ocr_res[0]["rec_texts"]
                det_word_cordnates: List[np.ndarray] = ocr_res[0]["rec_polys"]
                for index in range(len(accuracy_list)):
                    temp[rec_word_list[index]] = {
                        "score": accuracy_list[index],
                        "coordinates": det_word_cordnates[index].tolist(),
                    }
                data[f"page_{i + 1}"] = {
                    "ocr_results": temp,
                }
                print(f"Completed page {i+1}")
                idx += 1
        data["filename"] = Ufile.filename
        data["content_type"] = Ufile.content_type
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
        _ocr_model = _get_ocr_model()
        image_content = await UImage.read()
        nparr = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        ocr_res = _ocr_model.predict(image)
        # print(ocr_results[0]["rec_scores"])
        temp = {}
        accuracy_list = ocr_res[0]["rec_scores"]
        rec_word_list = ocr_res[0]["rec_texts"]
        det_word_cordnates: List[np.ndarray] = ocr_res[0]["rec_polys"]
        for index in range(len(accuracy_list)):
            temp[rec_word_list[index]] = {
                "score": accuracy_list[index],
                "coordinates": det_word_cordnates[index].tolist(),
            }
        data = {
            "filename": UImage.filename,
            "content_type": UImage.content_type,
            "results": temp,
        }
        return data
    except Exception as e:
        _release_ocr_model()
        return HTTPException(
            status_code=400,
            detail=str(e),
        )


# @router.post("/image_orientation", tags=["Image Orientation"])
# async def orienation_image(Ufile: UploadFile):
# try:
#     pass
# except RuntimeError as e:
#     return HTTPException(
#         status_code=500,
#         detail=f"Error loading OCR model: {str(e)}",
#     )
