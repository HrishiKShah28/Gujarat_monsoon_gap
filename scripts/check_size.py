import requests

url_hist = "https://nwdp.nwic.gov.in/dataset/535a095c-781e-407c-a6bd-52c6074789df/resource/8cc177be-e829-4b4d-88d1-549caa07d6a8/download/gwl_manual_quarterly_gujarat-sw-gw_gj_1991_2020.csv"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.head(url_hist, headers=headers, verify=False)
print("Content-Length header:", r.headers.get("Content-Length"))
if r.headers.get("Content-Length"):
    size_mb = int(r.headers.get("Content-Length")) / (1024*1024)
    print(f"File Size: {size_mb:.2f} MB")
