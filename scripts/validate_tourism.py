import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "tourism_clean.csv"

df = pd.read_csv(INPUT_FILE)

# 景點欄位：排除「月份」與「合計」
site_columns = list(df.columns[1:-1])

# 重新計算每月景點總和
df["計算合計"] = df[site_columns].sum(axis=1, min_count=1)

# 比較官方合計與計算合計
df["合計是否一致"] = df["合計"] == df["計算合計"]

print("=== 花蓮縣觀光遊憩區遊客資料驗證 ===")
print()

print(f"資料筆數：{len(df)}")
print(f"景點數量：{len(site_columns)}")
print()

print("=== 每月合計驗證 ===")

for _, row in df.iterrows():
    month = int(row["月份"])
    official = int(row["合計"])
    calculated = int(row["計算合計"])

    if official == calculated:
        print(f"✓ {month} 月：{official:,} = {calculated:,}")
    else:
        print(f"✗ {month} 月：官方 {official:,} ≠ 計算 {calculated:,}")

print()

# 檢查是否全部一致
if df["合計是否一致"].all():
    print("✓ 驗證通過：所有月份的合計皆一致")
    raise SystemExit(0)
else:
    print("✗ 驗證失敗：有月份的合計不一致")
    raise SystemExit(1)