from setuptools import setup, find_packages

setup(
    name="dashboard_finetuner_ppocr",
    version="0.1.0",
    description="Backend API for fine-tuning an OCR model via a dashboard UI.",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pylint",
        "black",
        "pre-commit",
        "requests",
    ],
    include_package_data=True,
)
