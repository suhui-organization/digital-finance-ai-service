"""Application configuration from environment variables."""

import os


class Config:
    # MiniMax API (OpenAI-compatible endpoint)
    # 文档: https://platform.minimax.chat
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "minimax")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "MiniMax-M1")
    API_KEY: str = os.getenv("API_KEY", "change-me-to-your-api-key")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.minimax.chat/v1")


config = Config()