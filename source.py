import requests
import re

# Config
URL = "http://livepptv.net/get.php?username=299819323222593&password=1593574628&type=m3u_plus&output=ts"
GROUP_WHITELIST = ["FRANCE H265", "FRANCE FHD", "FRANCE HD", "FRANCE SD", "SPORT FR", "SPORT AR", "ALGERIA", "ARABIC+", "ARABIC"]  # Change this to your desired groups
OUTPUT_FILE = "playlist.m3u"

# Download playlist
response = requests.get(URL)
data = response.text

# Split entries
entries = data.split("#EXTINF")
filtered_entries = []

for entry in entries:
    if 'group-title="' in entry:
        match = re.search(r'group-title="([^"]+)"', entry)
        if match:
            group = match.group(1)
            if group in GROUP_WHITELIST:
                filtered_entries.append("#EXTINF" + entry)

# Save result
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n" + "".join(filtered_entries))
