import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Default config filename
DEFAULT_CONFIG_FILE = "p115_cloud_downloader.config"

class Config:
    def __init__(self):
        self.P115_COOKIES = ""
        self.WATCH_DIR = ""
        self.PROCESSED_DIR = ""
        self.TARGET_PATH = ""
        self.TARGET_CID = ""
        self.LOG_LEVEL = "INFO"
        self.SUPPORTED_EXTENSIONS = []
        self.SETTLE_TIME = 1
        
        # Initial load with defaults
        self.load()

    def load(self, config_path=None):
        """Loads configuration from a file or environment variables."""
        if config_path:
            if not Path(config_path).exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
            load_dotenv(dotenv_path=config_path, override=True)
        elif Path(DEFAULT_CONFIG_FILE).exists():
            load_dotenv(dotenv_path=DEFAULT_CONFIG_FILE, override=True)
        else:
            load_dotenv(override=True)

        # Update attributes from environment variables
        self.P115_COOKIES = os.getenv("P115_COOKIES", "")
        self.WATCH_DIR = os.getenv("WATCH_DIR", str(Path(__file__).parent / "watch"))
        self.PROCESSED_DIR = os.getenv("PROCESSED_DIR", "processed")
        self.TARGET_PATH = os.getenv("TARGET_PATH", "/云下载")
        self.TARGET_CID = os.getenv("TARGET_CID", "")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        
        exts = os.getenv("SUPPORTED_EXTENSIONS", ".torrent,.magnet,.txt")
        self.SUPPORTED_EXTENSIONS = [ext.strip() for ext in exts.split(",") if ext.strip()]
        
        self.SETTLE_TIME = int(os.getenv("SETTLE_TIME", "1"))

    def validate(self):
        if not self.P115_COOKIES:
            if not Path(DEFAULT_CONFIG_FILE).exists() and not os.getenv("P115_COOKIES"):
                 raise ValueError(f"Configuration file '{DEFAULT_CONFIG_FILE}' not found. Please create it from the example.")
            raise ValueError("P115_COOKIES must be set in the config file or environment.")
        
        watch_path = Path(self.WATCH_DIR)
        if not watch_path.exists():
            watch_path.mkdir(parents=True, exist_ok=True)
            
        processed_path = watch_path / self.PROCESSED_DIR
        if not processed_path.exists():
            processed_path.mkdir(parents=True, exist_ok=True)

# Singleton instance
config = Config()
