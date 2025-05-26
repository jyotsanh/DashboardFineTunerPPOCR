from fastapi import APIRouter, UploadFile, File
from typing import Annotated

router = APIRouter()


@router.post("/upload", tags=["File Upload"])
async def upload_file(file: UploadFile):
    """
    Endpoint to upload a file.

    Args:
        file (bytes): The file content in bytes.

    Returns:
        dict: A confirmation message.
    """
    # Here you would typically save the file or process it
    return {"message": "File uploaded successfully"}


@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(Ufile: UploadFile):

    print(f"Content type: {Ufile.content_type}")
    data = {
        "filename": Ufile.filename,
        "content_type": Ufile.content_type,
        # "size": Ufile.spool_max_size,  # This is the maximum size of the file
    }
    return data
