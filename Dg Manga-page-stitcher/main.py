
"""
Save as: download_digest_pages.py
Requires: requests, beautifulsoup4, pillow
Install: pip install requests beautifulsoup4 pillow
"""

import os
import re
import base64
import io
import time
from PIL import Image
import requests
from bs4 import BeautifulSoup

# -------- CONFIG ----------


BASE_PAGE_URL = "https://thisaccessories.com/reading-base/?cat=183&paged={page}"
OUTPUT_DIR = r"E:\git-workstation\Web-Scraping-Lab\Dg Manga-page-stitcher\downloaded_pages"
START_PAGE = 6
END_PAGE = 218   # change to your total pages (e.g. 216)
REQUEST_DELAY = 0.8  # seconds between requests
MAX_RETRIES = 2       # 🔁 number of retry attempts
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36")

# JPEG Optimization Settings
JPEG_QUALITY = 85  # between 70–90 recommended for digest pages
# --------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

data_uri_re = re.compile(r"data:(image/[^;]+);base64,(.+)")

def fetch_page_html(page_num):
    url = BASE_PAGE_URL.format(page=page_num)
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def extract_images_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    imgs = []
    img_tags = soup.find_all("img")
    for tag in img_tags:
        src = tag.get("src")
        if not src:
            continue
        m = data_uri_re.match(src)
        if m:
            b64 = m.group(2)
            try:
                raw = base64.b64decode(b64)
                img = Image.open(io.BytesIO(raw)).convert("RGB")
                imgs.append(img)
            except Exception as e:
                print("  ❌ Failed to decode base64 image:", e)
        else:
            try:
                if src.startswith("//"):
                    src = "https:" + src
                elif src.startswith("/"):
                    src = "https://thisaccessories.com" + src
                rr = session.get(src, timeout=30)
                rr.raise_for_status()
                img = Image.open(io.BytesIO(rr.content)).convert("RGB")
                imgs.append(img)
            except Exception as e:
                print(f"  ❌ Failed to download image {src}: {e}")
    return imgs

def stitch_vertical(images):
    if not images:
        return None
    max_w = max(im.width for im in images)
    total_h = sum(im.height for im in images)
    dst = Image.new("RGB", (max_w, total_h), (255,255,255))
    y = 0
    for im in images:
        x = (max_w - im.width)//2 if im.width != max_w else 0
        dst.paste(im, (x, y))
        y += im.height
    return dst

def download_and_stitch_page(page_num):
    print(f"📥 Downloading page {page_num} ...")
    try:
        html = fetch_page_html(page_num)
        imgs = extract_images_from_html(html)
        if not imgs:
            print(f"  ⚠️ No images found on page {page_num}")
            return False
        stitched = stitch_vertical(imgs)
        if stitched:
            out_name = os.path.join(OUTPUT_DIR, f"page_{page_num:03d}.jpg")
            stitched.save(
                out_name,
                format="JPEG",
                quality=JPEG_QUALITY,
                optimize=True,
                progressive=True
            )
            print(f"  ✅ Saved {out_name} ({stitched.width}x{stitched.height})")
            return True
    except Exception as e:
        print(f"  ❌ Error on page {page_num}: {e}")
    return False

def main():
    failed_pages = []
    for p in range(START_PAGE, END_PAGE + 1):
        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            print(f"\n➡️ Attempt {attempt} for page {p}")
            if download_and_stitch_page(p):
                success = True
                break
            else:
                print(f"  🔁 Retrying page {p} after delay...")
                time.sleep(REQUEST_DELAY * 2)
        if not success:
            failed_pages.append(p)
        time.sleep(REQUEST_DELAY)

    print("\n" + "=" * 60)
    print("📊 DOWNLOAD SUMMARY")
    print(f"Total pages attempted: {END_PAGE - START_PAGE + 1}")
    print(f"Successful pages: {(END_PAGE - START_PAGE + 1) - len(failed_pages)}")
    print(f"Failed pages after {MAX_RETRIES} retries: {len(failed_pages)}")
    if failed_pages:
        print("❌ Missing / Failed pages:", ", ".join(map(str, failed_pages)))
        with open(os.path.join(OUTPUT_DIR, "failed_pages.txt"), "w") as f:
            f.write("\n".join(map(str, failed_pages)))
        print("📝 Failed pages list saved to 'failed_pages.txt'")
    else:
        print("✅ All pages downloaded successfully!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

