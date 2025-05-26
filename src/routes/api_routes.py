from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Annotated
from PyPDF2 import PdfReader
import io

router = APIRouter()

MAX_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_PAGES = 10


@router.post("/upload-pdf", tags=["File Upload"])
async def upload_file(Ufile: UploadFile):
    """
    Upload a PDF file and return its metadata.
    Args:
        Ufile (UploadFile): The file to be uploaded.
    Returns:
        dict: Metadata of the uploaded file, including filename and content type.
    """
    try:
        if (
            Ufile.content_type != "application/pdf" or Ufile.size > MAX_SIZE
        ):  # Check if the file is a PDF and within size limits
            return HTTPException(
                status_code=400,
                detail="Invalid file type. Only PDF files are allowed and size must be less than 10 MB.",
            )
        content = await Ufile.read()
        reader = PdfReader(io.BytesIO(content))
        if len(reader.pages) > MAX_PAGES:  # Check if the PDF has more than 10 pages
            return HTTPException(
                status_code=400,
                detail="PDF file exceeds the maximum allowed pages (10).",
            )
        data = {
            "filename": Ufile.filename,
            "content_type": Ufile.content_type,
            # "size": Ufile.spool_max_size,  # This is the maximum size of the file
        }
        return data
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail=str(e),
        )
