import requests


def calculate_risk(tx):
    risk = 0
    reasons = []

    fee = tx.get("fee", 0)
    size = tx.get("size", 0)
    inputs = len(tx.get("vin", []))
    outputs = len(tx.get("vout", []))

    # Fee rate
    fee_rate = fee / size if size > 0 else 0

    # Basic transaction-risk indicators
    if fee_rate > 100:
        risk += 20
        reasons.append("Unusually high fee rate")

    if inputs >= 20:
        risk += 20
        reasons.append("Very large number of inputs")

    if outputs >= 20:
        risk += 20
        reasons.append("Very large number of outputs")

    if size > 100000:
        risk += 20
        reasons.append("Very large transaction size")

    if inputs == 1 and outputs == 1:
        risk += 0

    # Limit score to 100
    risk = min(risk, 100)

    if risk >= 50:
        level = "HIGH RISK"
    elif risk >= 20:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return risk, level, reasons


txid = input("Enter Bitcoin Transaction ID (TXID): ").strip()

url = f"https://mempool.space/api/tx/{txid}"

try:
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("❌ Transaction not found.")
        exit()

    tx = response.json()

    print("\n✅ Live transaction found!")
    print("Transaction ID:", tx["txid"])
    print("Fee:", tx["fee"], "satoshis")
    print("Size:", tx["size"], "bytes")
    print("Weight:", tx["weight"])
    print("Inputs:", len(tx["vin"]))
    print("Outputs:", len(tx["vout"]))

    risk, level, reasons = calculate_risk(tx)

    print("\n================================")
    print("LIVE TRANSACTION RISK ANALYSIS")
    print("================================")

    print("Risk Score:", risk, "%")
    print("Risk Level:", level)

    if reasons:
        print("\nRisk indicators:")
        for reason in reasons:
            print("-", reason)
    else:
        print("\nNo unusual indicators detected.")

    print("\n⚠️ Risk score is not proof of fraud.")

except requests.exceptions.RequestException:
    print("❌ Unable to connect to Bitcoin network.")