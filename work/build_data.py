import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "tourism_clean.csv"
OUTPUT_FILE = ROOT / "docs" / "data.js"

# 讀取 ETL 後的資料
df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")

# 將 pandas 的 NaN 轉成 JavaScript 可用的 null
df = df.astype(object).where(pd.notna(df), None)

# 轉成網頁需要的資料格式
data = {
    "months": df["月份"].tolist(),
    "sites": list(df.columns[1:-1]),
    "records": df.to_dict(orient="records"),
}

# 寫成 JavaScript 檔案
OUTPUT_FILE.write_text(
    "window.TOURISM_DATA = "
    + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    + ";\n",
    encoding="utf-8",
)

print(f"完成：{OUTPUT_FILE}")
print(f"月份：{len(data['months'])}")
print(f"景點：{len(data['sites'])}")
print(f"資料筆數：{len(data['records'])}")
print(f"檔案大小：{OUTPUT_FILE.stat().st_size:,} bytes")