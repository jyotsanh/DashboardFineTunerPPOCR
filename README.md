# DashboardFineTunerPPOCR

This repo contains the backend API for the Dashboard frontend, which provides a user-friendly interface for fine-tuning an OCR model.

## Note:

- This repository follows [Black](https://black.readthedocs.io/en/stable/) code formatting.
- Before pushing or creating a pull request, please ensure you:

  1. Install `uv` package manager:

     ```bash
     curl -Ls https://astral.sh/uv/install.sh | bash
     ```

  2. Clone the repository:

     ```bash
     git clone https://github.com/jyotsanh/DashboardFineTunerPPOCR.git
     cd DashboardFineTunerPPOCR
     ```

  3. Set up the environment and install dependencies:

     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: .\venv\Scripts\activate
     uv sync                   # Installs dependencies defined in pyproject.toml or requirements.txt if configured
     ```

  4. Install pre-commit and set it up:

     ```bash
     pre-commit install
     ```

  5. Run Black formatting before committing:
     ```bash
     pre-commit run --all-files
     ```

Thank you for following the project conventions.
