"""Application configuration from environment variables."""

import os


class Config:
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "openai")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    API_KEY: str = os.getenv("API_KEY", "")


config = Config()