# P115 Cloud Downloader

A lightweight, automated tool to monitor a local directory for torrent files and magnet links and automatically submit them to your 115 Cloud offline download queue.

## Features

- **Automated Monitoring**: Real-time directory watching using `watchdog`.
- **Startup Sync**: Automatically scans and processes existing files in the monitored directory upon launch.
- **Format Support**: Handles `.torrent` files, `.magnet` files, and `.txt` files containing magnet links.
- **Smart File Management**: Successfully processed files are automatically moved to a `processed` subfolder to keep your workspace clean.
- **Customizable Target**: Configure your cloud target directory via path or CID.
- **Verbose Configuration**: Fully customizable via `p115-cloud-downloader.config`.

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
   cp p115-cloud-downloader.config.example p115-cloud-downloader.config
   ```

2. Edit `p115-cloud-downloader.config` with your settings:
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

## Development

Run tests:
```bash
uv run test_downloader.py
```

## License

MIT
