import requests
import pandas as pd
import io
import os
import sys

url_cgwb = "https://nwdp.nwic.gov.in/dataset/956add67-cba9-41a5-9d5c-96d73db44aef/resource/ef17ded9-be74-48e6-9359-f3a19daeea4a/download/gwl_manual_quarterly_cgwb_gj_2021_2025.csv"
headers = {"User-Agent": "Mozilla/5.0"}

print("Downloading full 2021-2025 CGWB Gujarat Groundwater dataset...")
r = requests.get(url_cgwb, headers=headers, verify=False, timeout=60)
df = pd.read_csv(io.StringIO(r.text), low_memory=False)

print(f"Total Rows: {len(df):,d}")
print(f"Total Columns: {len(df.columns)}")
print(f"Memory / Size: {len(r.content) / (1024*1024):.2f} MB")
print(f"Unique Stations: {df['Station'].nunique():,d}")
print(f"Unique Districts: {df['District'].nunique():,d}")
print(f"Districts List: {sorted(df['District'].dropna().unique().tolist())}")

# Parse Date
df['date'] = pd.to_datetime(df['Data Acquisition Time'], format='%d-%m-%Y %H:%M', errors='coerce')
print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
print("\nObservations by Year:")
print(df['year'].value_counts().sort_index())
print("\nObservations by Month:")
print(df['month'].value_counts().sort_index())

print("\nDepth Summary (meters below ground level):")
print(df['Groundwater Level Quarterly Manual (meter)'].describe())
