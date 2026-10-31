import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load processed dataset
data = pd.read_csv("dataset/combined_transactions_fixed.csv")

# First column = transaction ID
# Last column = transaction class
X = data.iloc[:, 1:-1]
y = data.iloc[:, -1]

# Convert labels to numbers
y = pd.to_numeric(y, errors="coerce")

# Remove rows where the label is missing
valid_rows = y.notna()

X = X.loc[valid_rows]
y = y.loc[valid_rows]

# Convert all feature columns to numeric
X = X.apply(pd.to_numeric, errors="coerce")

# Replace missing feature values
X = X.fillna(0)

# Convert Elliptic classes:
# 1 = illicit/fraud
# 2 = licit/not fraud
# 3 = unknown → remove
valid_classes = y.isin([1, 2])

X = X.loc[valid_classes]
y = y.loc[valid_classes]

# Convert labels:
# 1 → 1 (FRAUD)
# 2 → 0 (NOT FRAUD)
y = y.map({1: 1, 2: 0})

print("Data prepared successfully!")
print("Total transactions:", len(X))
print("Fraud transactions:", (y == 1).sum())
print("Not fraud transactions:", (y == 0).sum())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

print("\nTraining AI model...")

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, predictions)

print("\nModel trained successfully!")
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "models/crypto_fraud_model.pkl")

print("\nModel saved successfully!")
print("Location: models/crypto_fraud_model.pkl")