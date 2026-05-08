import logging
import hashlib
import bencode
from p115client import P115Client, check_response
from config import config

# logger = logging.getLogger(__name__)
logger = logging.getLogger("p115_downloader")

class P115Downloader:
    def __init__(self):
        self.client = P115Client(config.P115_COOKIES, app="web")
        self._target_cid = None

    def get_target_cid(self):
        """Resolves the target CID from path or config."""
        if self._target_cid is not None:
            return self._target_cid
        
        if config.TARGET_CID:
            self._target_cid = int(config.TARGET_CID)
            return self._target_cid

        # Resolve path to CID
        path = config.TARGET_PATH.strip("/")
        if not path:
            self._target_cid = 0
            return 0
        
        try:
            # Simple path resolution using fs_dir_getid if available
            # or walking through the path. 
            # fs_dir_getid usually expects a full path starting with /
            full_path = f"/{path}"
            resp = self.client.fs_dir_getid(full_path)
            if resp.get("id"):
                self._target_cid = int(resp["id"])
                logger.info(f"Resolved target path '{full_path}' to CID: {self._target_cid}")
                return self._target_cid
            else:
                logger.warning(f"Could not resolve path '{full_path}', using root (0)")
                return 0
        except Exception as e:
            logger.error(f"Error resolving path: {e}")
            return 0

    def add_torrent(self, torrent_path):
        """Adds a torrent file to 115 offline download."""
        cid = self.get_target_cid()
        logger.info(f"Adding torrent: {torrent_path} to CID: {cid}")
        try:
            # Calculate info_hash locally
            with open(torrent_path, 'rb') as f:
                torrent_data = bencode.decode(f.read())
                info_section = bencode.encode(torrent_data['info'])
                info_hash = hashlib.sha1(info_section).hexdigest()
                logger.info(f"Calculated info_hash: {info_hash}")

            # Prepare payload for offline_add_torrent
            # Based on documentation, it takes info_hash and wp_path_id
            payload = {
                "info_hash": info_hash,
                "wp_path_id": cid
            }
            resp = self.client.offline_add_torrent(payload)
            check_response(resp)
            if resp.get("state"):
                logger.info(f"Successfully added torrent task: {torrent_path}")
                return True
            else:
                logger.error(f"Failed to add torrent: {resp.get('error')}")
                return False
        except Exception as e:
            # Handle "Task already exists" error (10008) or "Invalid link" (10004)
            # 10004 can sometimes occur for duplicate magnets in some API versions
            if any(code in str(e) for code in ['10008', '10004']) or \
               (hasattr(e, 'args') and any(any(code in str(arg) for code in ['10008', '10004']) for arg in e.args)):
                logger.info(f"Torrent task already exists or invalid on 115: {torrent_path}")
                return True
            logger.error(f"Exception adding torrent: {e}")
            return False

    def add_magnet(self, magnet_link):
        """Adds a magnet link to 115 offline download."""
        cid = self.get_target_cid()
        logger.info(f"Adding magnet link to CID: {cid}")
        try:
            # Using offline_add_urls which supports wp_path_id
            payload = {
                "urls": magnet_link,
                "wp_path_id": cid
            }
            resp = self.client.offline_add_urls(payload)
            check_response(resp)
            if resp.get("state"):
                logger.info("Successfully added magnet task")
                return True
            else:
                logger.error(f"Failed to add magnet: {resp.get('error')}")
                return False
        except Exception as e:
            # Handle "Task already exists" error (10008) or "Invalid link" (10004)
            if any(code in str(e) for code in ['10008', '10004']) or \
               (hasattr(e, 'args') and any(any(code in str(arg) for code in ['10008', '10004']) for arg in e.args)):
                logger.info("Magnet task already exists or invalid on 115.")
                return True
            logger.error(f"Exception adding magnet: {e}")
            return False

# downloader = P115Downloader() # Removed to allow lazy instantiation
