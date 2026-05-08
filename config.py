import os
from pathlib import Path
from dotenv import load_dotenv

# Path to the custom config file
CONFIG_FILE = "p115-cloud-downloader.config"

# Load config from file if it exists
if Path(CONFIG_FILE).exists():
    load_dotenv(dotenv_path=CONFIG_FILE)
else:
    # Fallback to .env for backward compatibility
    load_dotenv()

class Config:
    # 115 Cookies (Required)
    P115_COOKIES = os.getenv("P115_COOKIES", "")
    
    # Local directory to watch
    WATCH_DIR = os.getenv("WATCH_DIR", str(Path(__file__).parent / "watch"))
    
    # Subdirectory for processed files
    PROCESSED_DIR = os.getenv("PROCESSED_DIR", "processed")
    
    # Target 115 directory path
    TARGET_PATH = os.getenv("TARGET_PATH", "/云下载")
    
    # Target 115 CID
    TARGET_CID = os.getenv("TARGET_CID", "")
    
    # Log Level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Supported Extensions
    _exts = os.getenv("SUPPORTED_EXTENSIONS", ".torrent,.magnet,.txt")
    SUPPORTED_EXTENSIONS = [ext.strip() for ext in _exts.split(",") if ext.strip()]
    
    # Settle time
    SETTLE_TIME = int(os.getenv("SETTLE_TIME", "1"))

    @classmethod
    def validate(cls):
        if not cls.P115_COOKIES:
            # Check if it's still the default example value
            if not Path(CONFIG_FILE).exists() and not os.getenv("P115_COOKIES"):
                 raise ValueError(f"Configuration file '{CONFIG_FILE}' not found. Please create it from the example.")
            raise ValueError("P115_COOKIES must be set in the config file.")
        
        watch_path = Path(cls.WATCH_DIR)
        if not watch_path.exists():
            print(f"Creating watch directory: {watch_path}")
            watch_path.mkdir(parents=True, exist_ok=True)
            
        processed_path = watch_path / cls.PROCESSED_DIR
        if not processed_path.exists():
            print(f"Creating processed directory: {processed_path}")
            processed_path.mkdir(parents=True, exist_ok=True)

config = Config
