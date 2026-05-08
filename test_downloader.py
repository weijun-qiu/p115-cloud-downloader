import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import os

# Set dummy env vars for testing
os.environ["P115_COOKIES"] = "uid=123;cid=456"
os.environ["WATCH_DIR"] = "./test_watch"

from downloader import P115Downloader

class TestDownloader(unittest.TestCase):
    @patch('downloader.P115Client')
    def test_add_magnet(self, mock_client_class):
        mock_client = mock_client_class.return_value
        mock_client.offline_add_url.return_value = {"state": True}
        mock_client.fs_dir_getid.return_value = {"id": "123"}
        
        dl = P115Downloader()
        magnet = "magnet:?xt=urn:btih:EXAMPLE"
        result = dl.add_magnet(magnet)
        
        self.assertTrue(result)
        mock_client.offline_add_url.assert_called_with(magnet, cid=123)
        mock_client.fs_dir_getid.assert_called_with("/云下载")

    @patch('downloader.P115Client')
    def test_add_torrent(self, mock_client_class):
        mock_client = mock_client_class.return_value
        mock_client.offline_add_torrent.return_value = {"state": True}
        mock_client.fs_dir_getid.return_value = {"id": "123"}
        
        dl = P115Downloader()
        torrent = "test.torrent"
        result = dl.add_torrent(torrent)
        
        self.assertTrue(result)
        mock_client.offline_add_torrent.assert_called_with(torrent, cid=123)

if __name__ == "__main__":
    unittest.main()
