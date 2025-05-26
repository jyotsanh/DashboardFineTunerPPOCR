import io

from fastapi import APIRouter, HTTPException, UploadFile
from PyPDF2 import PdfReader

from config.base import _get_ocr_model

router = APIRouter()

MAX_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_PAGES = 10


@router.post("/upload-pdf", tags=["File Upload"])
async def upload_file(Ufile: UploadFile):
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


@router.post("image_orientation", tags=["Image Orientation"])
async def orienation_image(Ufile: UploadFile):
    _get_ocr_model()
    # orientation_model.predict()
