"""Central configuration for the project.

Load settings from environment variables.
"""

import os
from dataclasses import dataclass


@dataclass
class Config:
    telegram_api_id: str = os.getenv("TELEGRAM_API_ID", "")
    telegram_api_hash: str = os.getenv("TELEGRAM_API_HASH", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")


cfg = Config()
