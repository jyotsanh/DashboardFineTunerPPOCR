from typing import Dict, Optional

from fastapi import APIRouter

from trainer import train_model

router = APIRouter()


@router.post("/train-model", tags=["Train OCR"])
async def train_ocr_model(user_id: str, data: Optional[Dict] = None):
    """Train an OCR model with the provided data.

    Args:
        user_id (str): User identifier from authentication.
        data (Optional[Dict[str]]): Data for training the OCR model.
    Returns:
        Dict[str, Any]: Training status and any additional information.
    """
    isSucess = train_model(user_id, data)
    # Placeholder for training logic
    if not isSucess:
        return {"status": "Training failed", "user_id": user_id, "data": data}

    return {"status": "Training started", "user_id": user_id, "data": data}


@router.post("/save", tags=["Train OCR"])
async def save_model():
    pass
