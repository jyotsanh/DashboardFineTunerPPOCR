from dotenv import load_dotenv
from paddleocr import PaddleOCR
from pydantic_settings import BaseSettings

SYSTEM_PATH = "/home/b0g0/product/DashboardFineTunerPPOCR/models"
ORIENTATION_MODEL_PATH = f"{SYSTEM_PATH}/official_models/PP-LCNet_x1_0_doc_ori"
TXT_DETECTION_MODEL_PATH = f"{SYSTEM_PATH}/official_models/PP-OCRv5_mobile_det"
TXT_RECGNTION_MODEL_PATH = f"{SYSTEM_PATH}/official_models/PP-OCRv5_mobile_rec"


def load_environment_variables(mode: str):
    env_file = f".env.{mode}" if mode in ["dev", "prod"] else ".env.dev"
    print(f"Loading environment variables from {env_file}")
    load_dotenv(env_file)


class BaseConfig(BaseSettings):
    API_KEY: str

    class Config:
        env_file_encoding = "utf-8"


# _SUPPORTED_OCR_VERSIONS = ["PP-OCRv3", "PP-OCRv4", "PP-OCRv5"]

_ocr_model = None


def _get_ocr_model():
    """Function that returns a singleton instance."""
    global _ocr_model
    if _ocr_model is None:
        _ocr_model = PaddleOCR(
            ocr_version="PP-OCRv5",  # Specify the OCR version
            lang="en",
            device="gpu",
            use_doc_orientation_classify=True,
            doc_orientation_classify_model_dir=ORIENTATION_MODEL_PATH,
            text_detection_model_dir=TXT_DETECTION_MODEL_PATH,
            text_recognition_model_dir=TXT_RECGNTION_MODEL_PATH,
            use_doc_unwarping=False,  # use_doc_unwarping
            use_textline_orientation=False,
        )

    return _ocr_model
