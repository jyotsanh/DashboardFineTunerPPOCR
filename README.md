# DashboardFineTunerPPOCR

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

  6. Install new python for specific project:

     ```bash
     # to list all available download able version
     uv python list --all-versions

     # to list all version available in you system:
     uv python list --only-installed

     # now pin the python to use open a project folder:
     uv python pin 3.9
     # then check if it's working or not by :
      uv python find
      # create venv using python 3.9
      uv venv  .venv

      # check if it's your installed version:
      python
     ```

Thank you for following the project conventions.

## How to run this project:

- ensure you have `.env.dev` and `.env.prod` file in root folder
  ```bash
  .env.dev # for development enviroments
  .env.prod # for production enviroments
  ```
- after activating the venv and installing all required package run the project:
  ```bash
  python src/server.py --run dev # for development
  python src/server.py --run prod # for production
  ```

## Project Details:

### Introduction:

- this is
