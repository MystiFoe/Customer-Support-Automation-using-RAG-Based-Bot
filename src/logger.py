import logging
import os
from typing import Optional
from config.settings import config


class Logger:
    def __init__(self, name: str, level: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level or config.logging.level)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(config.logging.file_path), exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(config.logging.file_path)
        file_handler.setFormatter(logging.Formatter(config.logging.format))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(config.logging.format))
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, *args, **kwargs) -> None:
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        self.logger.error(message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        self.logger.debug(message, *args, **kwargs)


def get_logger(name: str) -> Logger:
    return Logger(name)