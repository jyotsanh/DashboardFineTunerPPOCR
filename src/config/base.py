from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def load_environment_variables(mode: str):
    env_file = f".env.{mode}" if mode in ["dev", "prod"] else ".env.dev"
    print(f"Loading environment variables from {env_file}")
    load_dotenv(env_file)


class BaseConfig(BaseSettings):
    API_KEY: str

    class Config:
        env_file_encoding = "utf-8"
