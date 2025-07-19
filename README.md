# Recursive Web Directory Downloader

This tool recursively downloads all files from a web-based file index (like Apache/Nginx auto-index listings), including nested directories.

## Features
- Recursively follows directories
- Skips already existing files
- Optional dry-run mode to preview actions
- Optional delay to prevent server rate-limiting

## Requirements
Install required Python packages:

```bash
pip install -r requirements.txt
```

### Using a Virtual Environment (Recommended)
1. Create a virtual environment:

```bash
python3 -m venv venv
```

2. Activate it:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the script:

```bash
python recursive_web_downloader.py
```

### Example Configuration
Edit the script:

```python
base_url = 'http://example.com/Exchanges/'  # Replace with your actual URL
output_folder = 'downloaded_files'
dry_mode = True  # Set to False to enable actual downloading
download_directory(base_url, output_folder, dry_run=dry_mode, delay=1.0)
```

### Parameters
- `url`: The root URL of the web directory
- `local_dir`: The destination folder to save the mirrored content
- `dry_run`: If True, only prints planned downloads
- `delay`: Seconds to wait between file downloads

## Notes
- Designed for index-style pages (`Index of /folder/`)
- This script does not support authentication or JavaScript-heavy UIs

## License
MIT
