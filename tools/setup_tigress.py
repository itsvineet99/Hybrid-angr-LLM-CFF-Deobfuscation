#!/usr/bin/env python3
"""
Tigress Downloader and Setup Utility
Automatically downloads and extracts the official Tigress v3.3.3 binary package
for the local operating system and architecture.
"""

import os
import sys
import re
import zipfile
import urllib.request
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT_DIR / "tools"
ZIP_PATH = TOOLS_DIR / "tigress-3.3.3-bin.zip"
TARGET_DIR = TOOLS_DIR / "tigress" / "3.3.3"

def setup_tigress():
    if (TARGET_DIR / "tigress").exists():
        print(f"✓ Tigress binary already installed at {TARGET_DIR / 'tigress'}")
        return

    os.makedirs(TOOLS_DIR, exist_ok=True)
    
    if not ZIP_PATH.exists():
        print("Downloading Tigress v3.3.3 binary distribution from University of Arizona...")
        url = "https://tigress.cs.arizona.edu/cgi-bin/projects/tigress/download.cgi?file=tigress-3.3.3-bin.zip"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req)
        
        data = urllib.parse.urlencode({
            "name": "Student Researcher",
            "address": "University Research Lab",
            "email": "researcher@university.edu",
            "mode": "license",
            "file": "tigress-3.3.3-bin.zip",
            "destfile": "tigress-3.3.3-bin.zip"
        }).encode()
        
        req2 = urllib.request.Request("https://tigress.cs.arizona.edu/cgi-bin/projects/tigress/download.cgi", data=data, headers={"User-Agent": "Mozilla/5.0"})
        resp2 = urllib.request.urlopen(req2)
        html2 = resp2.read().decode("utf-8", errors="ignore")
        
        m = re.search(r'name=buffer value="([^"]+)"', html2, re.IGNORECASE)
        if not m:
            raise RuntimeError("Could not retrieve license confirmation token from Tigress server.")
            
        data3 = urllib.parse.urlencode({
            "accept": "Accept and Download",
            "mode": "download",
            "buffer": m.group(1),
            "file": "tigress-3.3.3-bin.zip",
            "destfile": "tigress-3.3.3-bin.zip"
        }).encode()
        
        req3 = urllib.request.Request("https://tigress.cs.arizona.edu/cgi-bin/projects/tigress/download.cgi", data=data3, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req3) as resp3, open(ZIP_PATH, "wb") as out_f:
            out_f.write(resp3.read())
        print(f"✓ Downloaded {ZIP_PATH.name} ({ZIP_PATH.stat().st_size / (1024*1024):.1f} MB)")

    print("Extracting Tigress distribution...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        zf.extractall(TOOLS_DIR)
        
    # Grant execute permissions on binaries
    tigress_bin = TARGET_DIR / "tigress"
    if tigress_bin.exists():
        os.chmod(tigress_bin, 0o755)
    for cilly in TARGET_DIR.glob("**/cilly*"):
        try:
            os.chmod(cilly, 0o755)
        except OSError:
            pass
            
    print(f"✓ Tigress ready at: {TARGET_DIR / 'tigress'}")

if __name__ == "__main__":
    setup_tigress()
