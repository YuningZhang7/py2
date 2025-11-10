# scotland_local_clean.py
import re
from pathlib import Path
import pandas as pd

# Scotland postcode areas (letter prefix)
SCOT_AREAS = {"AB","DD","DG","EH","FK","G","HS","IV","KA","KW","KY","ML","PA","PH","TD","ZE"}
# Common postcode column names
CANDIDATES = ["Outcode","Postcode","pcd","pcds","pcd7","pcd8"]
AREA_RE = re.compile(r"^([A-Z]{1,2})")

def _find_postcode_col(cols):
    lower = {c.lower(): c for c in cols}
    for k in CANDIDATES:
        if k.lower() in lower:
            return lower[k.lower()]
    for c in cols:
        lc = c.lower()
        if "post" in lc and "code" in lc:
            return c
    return None

def filter_scotland_by_area(df, postcode_col=None):
    col = postcode_col or _find_postcode_col(df.columns)
    if not col:
        raise KeyError("Postcode column not found. Pass postcode_col=...")
    s = df[col].astype(str).str.strip().str.upper()
    area = s.str.extract(AREA_RE, expand=False)
    return df.loc[area.isin(SCOT_AREAS)].copy()

def clean_file(input_path, output_path, postcode_col=None, chunksize=None, usecols=None):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if chunksize:
        first = True
        for chunk in pd.read_csv(input_path, dtype=str, chunksize=chunksize, usecols=usecols):
            sub = filter_scotland_by_area(chunk, postcode_col)
            if len(sub) == 0:
                continue
            sub.to_csv(output_path, index=False, mode="w" if first else "a", header=first)
            first = False
    else:
        df = pd.read_csv(input_path, dtype=str, usecols=usecols)
        sub = filter_scotland_by_area(df, postcode_col)
        sub.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    #Your local Windows paths
    INPUT_2018 = Path(r"D:\python project2\Postcode_level_all_meters_electricity_2018.csv")
    INPUT_2017 = Path(r"D:\python project2\Postcode_level_all_meters_electricity_2017.csv")

    OUTDIR = Path(r"D:\python project2\clean")
    OUT_2018 = OUTDIR / "electricity_scotland_2018.csv"
    OUT_2017 = OUTDIR / "electricity_scotland_2017.csv"

    # Run
    clean_file(INPUT_2018, OUT_2018)                  
    clean_file(INPUT_2017, OUT_2017, chunksize=200000)  # chunked example
