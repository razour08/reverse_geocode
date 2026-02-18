
import os
import shutil
import sys
from urllib.request import urlopen, Request

GEOCODE_URL = "http://download.geonames.org/export/dump/cities1000.zip"
ALTERNATE_NAMES_URL = "http://download.geonames.org/export/dump/alternateNames.zip"

def download_file(url, filename):
    print(f"Downloading {url} to {filename}...")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req) as response, open(filename, 'wb') as out_file:
            meta = response.info()
            file_size = int(meta.get("Content-Length", 0))
            print(f"File size: {file_size/1024/1024:.2f} MB")
            
            block_sz = 8192
            downloaded = 0
            while True:
                buffer = response.read(block_sz)
                if not buffer:
                    break
                downloaded += len(buffer)
                out_file.write(buffer)
                if file_size:
                    percent = downloaded * 100. / file_size
                    status = r"%10d  [%3.2f%%]" % (downloaded, percent)
                    status = status + chr(8)*(len(status)+1)
                    sys.stdout.write(status)
                    sys.stdout.flush()
        print("\nDownload complete.")
        return True
    except Exception as e:
        print(f"\nDownload failed: {e}")
        return False

if __name__ == "__main__":
    if not os.path.exists("cities1000.zip"):
        download_file(GEOCODE_URL, "cities1000.zip")
    else:
        print("cities1000.zip already exists.")
        
    if not os.path.exists("alternateNames.zip") or os.path.getsize("alternateNames.zip") < 100000000: # Assuming > 100MB
        print("alternateNames.zip missing or incomplete. Redownloading...")
        download_file(ALTERNATE_NAMES_URL, "alternateNames.zip")
    else:
        print("alternateNames.zip already exists.")
