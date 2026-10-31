import numpy as np
from sklearn.ensemble import IsolationForest


class LiveAIAnalyzer:

    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )

        self.is_trained = False

    def extract_features(self, tx):

        fee = float(tx.get("fee", 0))

        size = float(
            tx.get("vsize", tx.get("size", 0))
        )

        inputs = len(tx.get("vin", []))

        outputs = len(tx.get("vout", []))

        fee_rate = fee / size if size > 0 else 0

        return [
            fee,
            size,
            inputs,
            outputs,
            fee_rate
        ]

    def train(self, transactions):

        if len(transactions) < 5:
            return False

        features = np.array([
            self.extract_features(tx)
            for tx in transactions
        ])

        self.model.fit(features)

        self.is_trained = True

        return True

    def predict(self, tx):

        if not self.is_trained:
            return (
                0,
                "🟢 LOW RISK",
                "AI model not trained"
            )

        features = np.array([
            self.extract_features(tx)
        ])

        prediction = self.model.predict(features)[0]

        if prediction == -1:

            return (
                75,
                "🔴 HIGH RISK",
                "AI detected an unusual transaction pattern."
            )

        else:

            return (
                10,
                "🟢 LOW RISK",
                "AI detected a normal transaction pattern."
            )