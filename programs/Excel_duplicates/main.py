#!/usr/bin/env python3
"""
AUIS Members Deduplicator (tailored to columns: "Member Name", "Member Email")

- Dedupe by the 5-digit numeric ID just before the '@' in Member Email, e.g. zb25001@ -> 25001
- Keeps the FIRST occurrence of each ID
- Outputs:
    - <input>_cleaned.xlsx
    - <input>_duplicates.xlsx
    - <input>_summary.txt
"""

import os
import re
import pandas as pd

# ==== Edit this path to your local file ====
INPUT_PATH = r"/Users/zheer/Downloads/Updated.xlsx"   # e.g., r"C:\Users\you\Desktop\Old.xlsx"
SHEET_NAME = 0  # or "Sheet1" if needed

EMAIL_COL = "Member Email"
NAME_COL  = "Member Name"

ID_REGEX = re.compile(r'(\d{5})(?=@)', re.IGNORECASE)

def extract_id5(email: str):
    if not isinstance(email, str):
        return None
    m = ID_REGEX.search(email)
    if m:
        return m.group(1)
    try:
        local = email.split("@")[0]
        digits = "".join(ch for ch in local if ch.isdigit())
        return digits[-5:] if len(digits) >= 5 else None
    except Exception:
        return None

def main():
    base, ext = os.path.splitext(INPUT_PATH)
    out_clean = f"{base}_cleaned.xlsx"
    out_dups = f"{base}_duplicates.xlsx"
    out_summary = f"{base}_summary.txt"

    if ext.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(INPUT_PATH, sheet_name=SHEET_NAME)
    elif ext.lower() in [".csv", ".txt"]:
        df = pd.read_csv(INPUT_PATH)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    if EMAIL_COL not in df.columns:
        raise ValueError(f"Column '{EMAIL_COL}' not found. Columns: {list(df.columns)}")

    df["_id5"] = df[EMAIL_COL].map(extract_id5)

    # Treat missing IDs as unique by giving each a distinct placeholder
    placeholders = pd.Series([f"__NULL_{i}" for i in df.index], index=df.index)
    filled = df["_id5"].fillna(placeholders)

    keep_mask = ~filled.duplicated(keep="first")
    cleaned = df.loc[keep_mask].drop(columns=["_id5"])
    duplicates = df.loc[~keep_mask]

    with pd.ExcelWriter(out_clean, engine="openpyxl") as writer:
        cleaned.to_excel(writer, index=False, sheet_name="Unique")

    with pd.ExcelWriter(out_dups, engine="openpyxl") as writer:
        if not duplicates.empty:
            duplicates = duplicates.sort_values(by=["_id5", EMAIL_COL])
            duplicates.to_excel(writer, index=False, sheet_name="Duplicates")
        else:
            pd.DataFrame({"info": ["No duplicates found"]}).to_excel(writer, index=False, sheet_name="Duplicates")

    with open(out_summary, "w", encoding="utf-8") as f:
        f.write("=== AUIS Email Dedup Summary ===\n")
        f.write(f"Input rows: {len(df)}\n")
        f.write(f"Unique rows kept: {len(cleaned)}\n")
        f.write(f"Duplicates removed: {len(duplicates)}\n")
        f.write(f"Rows with invalid/missing ID: {int(df['_id5'].isna().sum())}\n")

    print("Done.")
    print("Cleaned ->", out_clean)
    print("Duplicates ->", out_dups)
    print("Summary ->", out_summary)

if __name__ == "__main__":
    main()
