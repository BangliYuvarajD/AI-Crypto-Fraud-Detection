import pandas as pd

input_file = "dataset/combined_transactions.csv"
output_file = "dataset/combined_transactions_fixed.csv"

data = pd.read_csv(input_file, header=None)

print("Original shape:", data.shape)

columns = ["txId"]

for i in range(1, 167):
    columns.append(f"feature_{i}")

columns.append("class")

if len(data.columns) != len(columns):
    print(
        f"ERROR: CSV has {len(data.columns)} columns, "
        f"but expected {len(columns)} columns."
    )
else:
    data.columns = columns

    data.to_csv(output_file, index=False)

    print("CSV header fixed successfully!")
    print("Columns:", len(data.columns))
    print("Rows:", len(data))
    print("Saved to:", output_file)