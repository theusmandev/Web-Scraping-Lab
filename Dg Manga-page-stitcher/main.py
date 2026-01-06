
import os
import re
import base64
import io
import time
from PIL import Image
import requests
from bs4 import BeautifulSoup

# -------- CONFIG ----------
BASE_PAGE_URL = "https://thisaccessories.com/reading-base/?cat=180&paged={page}"
OUTPUT_DIR = "downloaded_pages"
START_PAGE = 1
END_PAGE = 1  # change if you want fewer pages while testing
REQUEST_DELAY = 0.8  # seconds between requests to be polite
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36")
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
    """
    Return list of PIL.Image objects in the same order they appear in the HTML.
    Handles:
      - data:image/...;base64,.....  (embedded pieces)
      - regular absolute/relative image URLs (downloads them)
    """
    soup = BeautifulSoup(html, "html.parser")
    imgs = []
    img_tags = soup.find_all("img")
    for tag in img_tags:
        src = tag.get("src")
        if not src:
            continue
        # If src is a data URI
        m = data_uri_re.match(src)
        if m:
            b64 = m.group(2)
            try:
                raw = base64.b64decode(b64)
                img = Image.open(io.BytesIO(raw)).convert("RGB")
                imgs.append(img)
            except Exception as e:
                print("  ❌ Failed to decode data URI image:", e)
        else:
            # regular URL: make it absolute if needed
            try:
                if src.startswith("//"):
                    src = "https:" + src
                elif src.startswith("/"):
                    # derive domain from known page
                    src = "https://thisaccessories.com" + src
                # download image
                rr = session.get(src, timeout=30)
                rr.raise_for_status()
                img = Image.open(io.BytesIO(rr.content)).convert("RGB")
                imgs.append(img)
            except Exception as e:
                print(f"  ❌ Failed to download image {src}: {e}")
    return imgs

def stitch_vertical(images):
    """Stitch list of PIL.Image vertically into one image, preserving width by expanding smaller images."""
    if not images:
        return None
    # Determine max width
    max_w = max(im.width for im in images)
    total_h = sum(im.height for im in images)
    dst = Image.new("RGB", (max_w, total_h), (255,255,255))
    y = 0
    for im in images:
        if im.width != max_w:
            # center the image horizontally
            x = (max_w - im.width)//2
        else:
            x = 0
        dst.paste(im, (x, y))
        y += im.height
    return dst

def download_and_stitch_page(page_num):
    print(f"Downloading page {page_num} ...")
    html = fetch_page_html(page_num)
    imgs = extract_images_from_html(html)
    if not imgs:
        print(f"  ⚠️ No images found on page {page_num}")
        return False
    stitched = stitch_vertical(imgs)
    if stitched:
        out_name = os.path.join(OUTPUT_DIR, f"page_{page_num:03d}.png")
        stitched.save(out_name, format="PNG")
        print(f"  ✅ Saved {out_name} ({stitched.width}x{stitched.height})")
        return True
    return False

def main():
    for p in range(START_PAGE, END_PAGE+1):
        try:
            ok = download_and_stitch_page(p)
        except Exception as e:
            print(f"Error on page {p}: {e}")
        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    main()

