import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/crypto_fraud_model.pkl")

# Load the feature dataset
features = pd.read_csv("dataset/elliptic_txs_features.csv")

# Remove transaction ID
X = features.iloc[:, 1:]

# Convert features to numeric
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

print("Crypto Fraud Detection System")
print("-----------------------------")
print("Number of available transactions:", len(X))

# Select one transaction for testing
transaction_number = int(input("Enter transaction number: "))

# Get transaction features
transaction = X.iloc[[transaction_number]]

# Make prediction
prediction = model.predict(transaction)[0]
probability = model.predict_proba(transaction)[0]

print("\n-----------------------------")

if prediction == 1:
    print("🔴 FRAUD / SUSPICIOUS TRANSACTION")
else:
    print("🟢 NOT FRAUD / LOW RISK TRANSACTION")

print(f"Fraud probability: {probability[1] * 100:.2f}%")
print("-----------------------------")