import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import config
from downloader import P115Downloader

# Global downloader instance
_downloader = None

def get_downloader():
    global _downloader
    if _downloader is None:
        _downloader = P115Downloader()
    return _downloader

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TorrentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        self.process_file(file_path)

    def process_file(self, file_path):
        # Ignore files in the processed subdirectory
        if config.PROCESSED_DIR in file_path.parts:
            return

        # Ignore temporary files (like .part or .crdownload)
        if file_path.suffix in ['.part', '.crdownload', '.tmp']:
            return

        logger.info(f"New file detected: {file_path}")
        
        # Give the file a moment to be fully written
        time.sleep(config.SETTLE_TIME)

        success = False
        if file_path.suffix == '.torrent' and '.torrent' in config.SUPPORTED_EXTENSIONS:
            success = get_downloader().add_torrent(str(file_path))
        elif file_path.suffix in config.SUPPORTED_EXTENSIONS:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content.startswith('magnet:?xt=urn:btih:'):
                        success = get_downloader().add_magnet(content)
                    else:
                        logger.debug(f"File {file_path} does not contain a valid magnet link.")
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")

        if success:
            self.move_to_processed(file_path)

    def move_to_processed(self, file_path):
        try:
            processed_dir = Path(config.WATCH_DIR) / config.PROCESSED_DIR
            target_path = processed_dir / file_path.name
            
            # Handle filename collisions
            if target_path.exists():
                target_path = processed_dir / f"{file_path.stem}_{int(time.time())}{file_path.suffix}"
            
            file_path.rename(target_path)
            logger.info(f"Moved {file_path.name} to {config.PROCESSED_DIR}/")
        except Exception as e:
            logger.error(f"Error moving file to processed: {e}")

def main():
    try:
        config.validate()
    except ValueError as e:
        logger.error(e)
        return

    watch_dir = Path(config.WATCH_DIR)
    logger.info(f"Starting monitor on: {watch_dir}")

    event_handler = TorrentHandler()

    # Process existing files first
    logger.info("Scanning for existing files...")
    for file_path in watch_dir.iterdir():
        if file_path.is_file():
            event_handler.process_file(file_path)

    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
