import requests
import io
import pandas as pd
import sys

url_cgwb = "https://nwdp.nwic.gov.in/dataset/956add67-cba9-41a5-9d5c-96d73db44aef/resource/ef17ded9-be74-48e6-9359-f3a19daeea4a/download/gwl_manual_quarterly_cgwb_gj_2021_2025.csv"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

print(f"Connecting to NWIC CGWB Gujarat Groundwater dataset...")
try:
    # Stream the first 50KB to inspect columns
    r = requests.get(url_cgwb, headers=headers, stream=True, timeout=20, verify=False)
    print(f"Status Code: {r.status_code}")
    content_chunks = []
    total_bytes = 0
    for chunk in r.iter_content(chunk_size=10240):
        content_chunks.append(chunk)
        total_bytes += len(chunk)
        if total_bytes > 50000:
            break
    sample_text = b"".join(content_chunks).decode("utf-8", errors="replace")
    print(f"Downloaded {total_bytes} bytes sample.")
    df_sample = pd.read_csv(io.StringIO(sample_text), low_memory=False)
    print("\nColumns:", df_sample.columns.tolist())
    print("\nFirst 3 rows:")
    print(df_sample.head(3).T)
except Exception as e:
    print(f"Error fetching NWIC data: {e}", file=sys.stderr)
