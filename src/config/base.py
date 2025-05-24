import os
from dotenv import load_dotenv

from typing import Optional, List
from pydantic import BaseModel


class BaseConfig(BaseModel):
    API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
