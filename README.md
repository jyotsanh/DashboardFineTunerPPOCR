# ashboardFineTunerPPOCR

This repo contains the backend API for the Dashboard frontend, which provides a user-friendly interface for fine-tuning an OCR model.

## Note:

- This repository follows [Black](https://black.readthedocs.io/en/stable/) code formatting.
- Before pushing or creating a pull request, please ensure you:
- This project use `uv` as package manager, if you want to know more about this package manager click [here](https://github.com/astral-sh/uv)

  1. Install `uv` package manager:

     ```bash
      # for linux/mac
      curl -Ls https://astral.sh/uv/install.sh | bash
      # for windows
      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

  2. Clone the repository:

     ```bash
      git clone https://github.com/jyotsanh/DashboardFineTunerPPOCR.git
      cd DashboardFineTunerPPOCR
     ```

  3. Set up the environment and install dependencies:

     ```bash
     python -m venv .venv                            # or uv venv .venv
     source venv/bin/activate                        # On Windows: .\venv\Scripts\activate
     uv pip sync requirements.txt                    # Installs dependencies defined in pyproject.toml or requirements.txt if configured
     uv pip tree                                         # View the dependency tree for the project
     ```

  4. Install pre-commit and set it up:

     ```bash
     pre-commit install
     ```

  5. Run Black formatting before committing:

     ```bash
     # before commiting anything please make you pass the black test
     pre-commit run --all-files
     ```

Thank you for following the project conventions.
