from paddleocr import PaddleOCR

# _SUPPORTED_OCR_VERSIONS = ["PP-OCRv3", "PP-OCRv4", "PP-OCRv5"]

SYSTEM_PATH = "/home/b0g0/product/DashboardFineTunerPPOCR/models"

ORIENTATION_MODEL_PATH = f"{SYSTEM_PATH}/official_models/PP-LCNet_x1_0_doc_ori"
TXT_DETECTION_MODEL_PATH = f"{SYSTEM_PATH}/official_models/PP-OCRv5_mobile_det"
TXT_RECGNTION_MODEL_PATH = f"{SYSTEM_PATH}/official_models/PP-OCRv5_mobile_rec"
model = PaddleOCR(
    ocr_version="PP-OCRv5",  # Specify the OCR version
    lang="en",
    device="gpu",
    use_doc_orientation_classify=True,
    doc_orientation_classify_model_dir=ORIENTATION_MODEL_PATH,
    text_detection_model_dir=TXT_DETECTION_MODEL_PATH,
    text_recognition_model_dir=TXT_RECGNTION_MODEL_PATH,
    use_doc_unwarping=False,  # 通过 use_doc_unwarping 参数指定不使用文本图像矫正模型
    use_textline_orientation=False,
)

results = model.predict("data/images/test_01.png")


for res in results:
    res.save_to_img("data/results/test_01.png")
    res.save_to_json("data/results/test_01.json")
