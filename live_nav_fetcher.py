import os
import requests
import pandas as pd

BASE_URL = "https://api.mfapi.in/mf/"
SCHEMES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

def fetch_and_save_nav(scheme_code, scheme_name):
    url = f"{BASE_URL}{scheme_code}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "data" in data and data["data"]:
            df = pd.DataFrame(data["data"])
            df["scheme_code"] = scheme_code
            df["scheme_name"] = scheme_name
            os.makedirs("data/raw", exist_ok=True)
            file_path = f"data/raw/{scheme_name}_raw.csv"
            df.to_csv(file_path, index=False)
            print(f"✓ Saved live data for {scheme_name}")
    except Exception as e:
        print(f"Error fetching {scheme_code}: {e}")

if __name__ == "__main__":
    for code, name in SCHEMES.items():
        fetch_and_save_nav(code, name)