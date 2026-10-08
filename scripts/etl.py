import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "007d32a4-2308-40ef-b888-32d25f59d3aa.csv"
OUTPUT_FILE = BASE_DIR / "data" / "tourism_clean.csv"

# 讀取原始資料
df = pd.read_csv(INPUT_FILE, na_values=["-"])

# 移除「合計」列
monthly = df[df["月份"] != "合計"].copy()

# 月份轉成數字
monthly["月份"] = pd.to_numeric(monthly["月份"], errors="coerce")

# 景點欄位
site_columns = list(monthly.columns[1:-1])

# 景點數字轉成數值
for col in site_columns:
    monthly[col] = pd.to_numeric(monthly[col], errors="coerce")

# 移除完全沒有資料的月份
monthly = monthly.dropna(subset=site_columns, how="all")

# 重新計算每月合計
monthly["合計"] = monthly[site_columns].sum(axis=1, min_count=1)

# 將有數值的欄位轉成整數格式，保留缺失值
for col in site_columns + ["合計"]:
    monthly[col] = monthly[col].astype("Int64")

# 輸出清理後資料
monthly.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"ETL 完成：{OUTPUT_FILE}")
print(f"資料筆數：{len(monthly)}")
print(f"欄位數：{len(monthly.columns)}")