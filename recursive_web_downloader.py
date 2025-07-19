import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

download_count = 0

def download_directory(url: str, local_dir: str, dry_run: bool = False, delay: float = 1.0, allowed_exts=None, skip_dirs=None):
    global download_count

    allow_all = allowed_exts is None or allowed_exts == ['*']
    if not allow_all:
        allowed_exts = [ext.lower() for ext in allowed_exts]

    skip_dirs = set(name.lower() for name in (skip_dirs or []))

    print(f"[INFO] Accessing: {url}")

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select('a[href]')
    for link in links:
        href = link['href']
        if href in ('../', './'):
            continue

        full_url = urljoin(url, href)
        path = urlparse(full_url).path
        filename = os.path.basename(path.rstrip('/'))
        local_path = os.path.join(local_dir, filename)

        if href.endswith('/'):
            if filename.lower() in skip_dirs:
                print(f"[SKIP DIR] {filename} (in skip list)")
                continue
            download_directory(full_url, local_path, dry_run=dry_run, delay=delay, allowed_exts=allowed_exts if not allow_all else ['*'], skip_dirs=skip_dirs)
        else:
            file_ext = os.path.splitext(filename)[1][1:].lower()
            if not allow_all and file_ext not in allowed_exts:
                print(f"[SKIP] {filename} (not an allowed type)")
                continue

            if os.path.exists(local_path):
                print(f"[SKIP] {local_path} already exists")
                continue

            if dry_run:
                print(f"[DRY RUN] Would download: {full_url} -> {local_path}")
                download_count += 1
            else:
                os.makedirs(local_dir, exist_ok=True)
                print(f"[DOWNLOADING] {full_url} -> {local_path}")
                with requests.get(full_url, stream=True) as r:
                    r.raise_for_status()
                    with open(local_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                time.sleep(delay)

if __name__ == '__main__':
    # Example usage:
    base_url = 'http://example.com/ABC/XYZ/'  # Replace with your actual URL
    output_folder = 'downloaded_files'
    dry_mode = False  # Set to False to enable actual downloading
    # extensions = ['*']  # Use ['*'] to download everything
    extensions = ['pdf']
    skip_folders = ['OLD', 'ARCHIVE']
    download_directory(base_url, output_folder, dry_run=dry_mode, delay=1.0, allowed_exts=extensions, skip_dirs=skip_folders)

    if dry_mode:
        print(f"[SUMMARY] Total files that would be downloaded: {download_count}")
