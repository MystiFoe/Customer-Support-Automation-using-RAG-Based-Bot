import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class OpenAIConfig:
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 500
    api_key: str = os.getenv("OPENAI_API_KEY", "")


@dataclass
class UIConfig:
    page_title: str = "AI Customer Support"
    page_icon: str = "🤖"
    layout: str = "wide"
    theme: str = "light"


@dataclass
class LoggingConfig:
    level: str = "INFO"
    file_path: str = "logs/app.log"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class AppConfig:
    openai: OpenAIConfig = OpenAIConfig()
    ui: UIConfig = UIConfig()
    logging: LoggingConfig = LoggingConfig()
    knowledge_base_path: str = "data/knowledge_base.json"


# Global configuration instance
config = AppConfig()