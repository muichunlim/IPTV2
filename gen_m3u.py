import requests
import time
import random
import re
from collections import OrderedDict

INPUT_URL = "https://tv.iill.top/m3u/Gather"
OUTPUT_FILE = "tv.m3u"

GROUP_ORDER = [
    "海外",
    "台灣",
    "台湾",
    "港澳",
    "綜合",
    "體育",
    "地方",
]

group_entries = OrderedDict((g, []) for g in GROUP_ORDER)

MAX_RETRIES = 2
for attempt in range(MAX_RETRIES + 1):
    try:
        headers = {
            "User-Agent": "VLC/3.0.20 LibVLC/3.0.20",
            "Referer": "https://live.catvod.com/",
            "Accept": "*/*"
        }
        resp = requests.get(INPUT_URL, headers=headers, timeout=20)
        resp.raise_for_status()
        if not resp.text:
            raise Exception("Response is empty")
        if len(resp.text.splitlines()) < 100:
            raise Exception("Response is less than 100 lines")
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < MAX_RETRIES:
            wait_seconds = random.randint(1, 300)
            print(f"Retrying in {wait_seconds} seconds...")
            time.sleep(wait_seconds)
        else:
            print("Fetch failed. Exiting.")
            exit(1)

# Save original m3u
with open("origin_tv.m3u", "wb") as f:
    f.write(resp.content)
lines = resp.text.splitlines()

i = 0
while i < len(lines) - 1:
    line = lines[i].strip()
    if not line.startswith("#EXTINF"):
        i += 1
        continue

    url = lines[i + 1].strip()

    # 提取 group-title
    group_match = re.search(r'group-title="([^"]*)"', line)
    if not group_match:
        i += 2
        continue

    group = group_match.group(1)

    matched_group = None
    for g in GROUP_ORDER:
        if g in group:
            matched_group = g
            break
            
    if not matched_group:
        i += 2
        continue

    group_entries[matched_group].append(f"{line}\n{url}\n")
    i += 2

# 输出新的 m3u
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="https://epg.iill.top/epg.xml.gz" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"\n')
    for group in GROUP_ORDER:
        if group_entries[group]:
            f.write('\n')
        for entry in group_entries[group]:
            f.write(entry)

print(f"Done. Output file: {OUTPUT_FILE}")
