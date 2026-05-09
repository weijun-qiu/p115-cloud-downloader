# P115 Cloud Downloader

A lightweight, automated tool to monitor a local directory for torrent files and magnet links and automatically submit them to your 115 Cloud offline download queue.

## Features

- **Automated Monitoring**: Real-time directory watching using `watchdog`.
- **Startup Sync**: Automatically scans and processes existing files in the monitored directory upon launch.
- **Format Support**: Handles `.torrent` files, `.magnet` files, and `.txt` files containing magnet links.
- **Smart File Management**: Successfully processed files are automatically moved to a `processed` subfolder to keep your workspace clean.
- **Customizable Target**: Configure your cloud target directory via path or CID.
- **Verbose Configuration**: Fully customizable via `p115_cloud_downloader.config`.

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

## Installation

### Using uv (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/p115-cloud-downloader.git
   cd p115-cloud-downloader
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Using pip

1. Clone the repository and navigate to the folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: You can generate requirements.txt using `uv export -o requirements.txt` if needed)*

## Configuration

1. Copy the example configuration file:
   ```bash
   cp p115_cloud_downloader.config.example p115_cloud_downloader.config
   ```

2. Edit `p115_cloud_downloader.config` with your settings:
   - **P115_COOKIES**: Your 115.com login cookies.
   - **WATCH_DIR**: Local folder to monitor (default: `./watch`).
   - **TARGET_PATH**: Cloud folder path (default: `/云下载`).
   - **LOG_LEVEL**: Logging verbosity (default: `INFO`).

Start the downloader:

```bash
uv run main.py
```

Or using standard python:

```bash
python main.py
```

### Custom Configuration Path

You can specify a custom configuration file using the `--config` argument:

```bash
python main.py --config /path/to/your/custom.config
```

The application will:
1. Scan the `WATCH_DIR` for any existing files and process them.
2. Start monitoring `WATCH_DIR` for new additions.
3. Move successfully added tasks to `WATCH_DIR/processed`.

### Running as a Systemd Service (Linux)

A template service file is provided: `p115-cloud-downloader.service.example`.

1. Copy the template to the systemd directory:
   ```bash
   sudo cp p115-cloud-downloader.service.example /etc/systemd/system/p115-cloud-downloader.service
   ```

2. Edit the service file to match your environment:
   - Change `User` and `Group`.
   - Update `WorkingDirectory` and `ExecStart` paths.

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable p115-cloud-downloader.service
   sudo systemctl start p115-cloud-downloader.service
   ```

## Development

Run tests:
```bash
uv run test_downloader.py
```

## License

MIT
