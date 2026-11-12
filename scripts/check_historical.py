import requests
import pandas as pd
import io
import os
import sys

url_hist = "https://nwdp.nwic.gov.in/dataset/535a095c-781e-407c-a6bd-52c6074789df/resource/8cc177be-e829-4b4d-88d1-549caa07d6a8/download/gwl_manual_quarterly_gujarat-sw-gw_gj_1991_2020.csv"
headers = {"User-Agent": "Mozilla/5.0"}

print("Checking historical 1991-2020 Gujarat Groundwater dataset...")
try:
    r = requests.get(url_hist, headers=headers, verify=False, stream=True, timeout=30)
    print(f"Status: {r.status_code}")
    # Read first 100KB
    chunks = []
    tot = 0
    for c in r.iter_content(chunk_size=10240):
        chunks.append(c)
        tot += len(c)
        if tot > 100000:
            break
    txt = b"".join(chunks).decode("utf-8", errors="replace")
    df_h = pd.read_csv(io.StringIO(txt), low_memory=False)
    print("Columns:", df_h.columns.tolist())
    print(df_h.head(2).T)
except Exception as e:
    print(f"Error: {e}")

