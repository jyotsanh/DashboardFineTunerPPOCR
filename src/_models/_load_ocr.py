import gc
from typing import Optional

from paddleocr import PaddleOCR, PPStructureV3

# _SUPPORTED_OCR_VERSIONS = ["PP-OCRv3", "PP-OCRv4", "PP-OCRv5"]
SYS_PATH = "/home/b0g0/product/DashboardFineTunerPPOCR/models"
ORIENTATION_MODEL_PATH = f"{SYS_PATH}/official_models/PP-LCNet_x1_0_doc_ori"
TXT_DETECTION_MODEL_PATH = f"{SYS_PATH}/official_models/PP-OCRv5_server_det"
TXT_RECGNTION_MODEL_PATH = f"{SYS_PATH}/official_models/PP-OCRv5_server_rec"
TXT_IMG_UNWRAPING_MODEL_PATH = f"{SYS_PATH}/official_models/UVDoc"
TXT_LINE_ORIENTATION_MDL_PATH = (
    f"{SYS_PATH}/official_models/PP-LCNet_x0_25_textline_ori"
)
LIT_DET_MDL_PATH = f"{SYS_PATH}/official_models/mobile_vers/OCRv5_mobile_det"
LIT_REC_MDL_PATH = f"{SYS_PATH}/official_models/mobile_vers/OCRv5_mobile_rec"

SERVER_DET_MDL_PATH = f"{SYS_PATH}/official_models/PP-OCRv5_server_det"
SERVER_REC_MDL_PATH = f"{SYS_PATH}/official_models/PP-OCRv5_server_rec"

DOC_BLOCK_LAYOUT_PATH = "f{SYS_PATH}/official_models/PP-DocBlockLayout"
DOC_LAYOUT_PLUS_L = "f{SYS_PATH}/official_models/PP-DocLayout_plus-L"

# Text Image Orientation Model:
# - This model mainly distinguishes the orientation of the document image
#    corrects it through post-processing
# - sometimes the camera is rotated to make the image clearer, resulting
#   in images with different orientations


# Text Image Correction/Unwarping Model:
# - The main purpose of text image correction is to perform geometric
#   transformation on the image to correct problems such as document
#   distortion, tilt, perspective deformation, etc. in the image,


# Text line orientation classification Model:
# - The main purpose of text line orientation classification is to
#   determine the orientation of text lines in the image, It makes sure
#   that the text lines are correctly oriented before recognition.
#   it ensures each line is read in the correct direction
#   (e.g., left-to-right, top-to-bottom).


# Text Detection Model:
# Text Recognition Model:

_ocr_model: Optional[PaddleOCR] = None


def _get_ocr_model():
    """Function that returns a singleton instance."""
    global _ocr_model
    if _ocr_model is None:
        try:
            _ocr_model = PaddleOCR(
                ocr_version="PP-OCRv5",  # Specify the OCR version
                lang="en",
                use_doc_orientation_classify=True,
                doc_orientation_classify_model_dir=ORIENTATION_MODEL_PATH,
                use_doc_unwarping=True,  # use_doc_unwarping
                doc_unwarping_model_dir=TXT_IMG_UNWRAPING_MODEL_PATH,
                use_textline_orientation=True,
                text_line_orientation_model_dir=TXT_LINE_ORIENTATION_MDL_PATH,
                text_detection_model_dir=LIT_DET_MDL_PATH,
                text_recognition_model_dir=LIT_REC_MDL_PATH,
            )
            print("loading............")
        except Exception as e:
            raise RuntimeError(f"Failed to load OCR model: {str(e)}")
    print("loading ocr model from cache")
    return _ocr_model


def _release_ocr_model():
    """Release OCR model from memory."""
    global _ocr_model
    if _ocr_model is not None:
        try:
            # Try to explicitly delete the model
            del _ocr_model
            _ocr_model = None

            # Clear GPU memory
            try:
                import torch

                if torch.cuda.is_available():
                    print("Releasing GPU memory...")
                    torch.cuda.empty_cache()
            except ImportError:
                pass

            try:
                import paddle

                paddle.device.cuda.empty_cache()
                print("Releasing PaddleOCR GPU memory...")
            except (ImportError, AttributeError):
                pass

            # Force garbage collection
            gc.collect()

        except Exception as e:
            print(f"Warning: Error releasing OCR model: {e}")
            _ocr_model = None


pipeline: Optional[PPStructureV3] = None


def _get_structure_ocr_model():
    "Function that returns a singleton instance of the structure OCR model."
    global pipeline
    if pipeline is None:
        try:
            pipeline = PPStructureV3(
                use_doc_orientation_classify=True,
                doc_orientation_classify_model_dir=ORIENTATION_MODEL_PATH,
                use_doc_unwarping=True,  # use_doc_unwarping
                doc_unwarping_model_dir=TXT_IMG_UNWRAPING_MODEL_PATH,
                textline_orientation_model_dir=TXT_LINE_ORIENTATION_MDL_PATH,
                text_detection_model_dir=SERVER_DET_MDL_PATH,
                text_recognition_model_dir=SERVER_REC_MDL_PATH,
            )

            print("loading............")
        except Exception as e:
            raise RuntimeError(f"Failed to load OCR model: {str(e)}")
    print("loading ocr model from cache")
    return pipeline
