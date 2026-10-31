import pandas as pd

# Load dataset
features = pd.read_csv("dataset/elliptic_txs_features.csv")
classes = pd.read_csv("dataset/elliptic_txs_classes.csv")

# Rename the first column for merging
features = features.rename(columns={features.columns[0]: "txId"})
classes = classes.rename(columns={classes.columns[0]: "txId"})

# Merge transaction features with their labels
data = features.merge(classes, on="txId")

print("Combined dataset shape:", data.shape)

print("\nColumns:")
print(data.columns.tolist())

print("\nClass distribution:")
print(data.iloc[:, -1].value_counts())

# Save the combined dataset
data.to_csv("dataset/combined_transactions.csv", index=False)

print("\nCombined dataset saved successfully!")