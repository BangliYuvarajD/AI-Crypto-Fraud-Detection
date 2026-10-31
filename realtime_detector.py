import requests

print("=== Real-Time Bitcoin Transaction Checker ===")

txid = input("Enter Bitcoin Transaction ID (TXID): ").strip()

url = f"https://mempool.space/api/tx/{txid}"

response = requests.get(url, timeout=10)

if response.status_code == 200:
    tx = response.json()

    print("\nTransaction found! ✅")
    print("Transaction ID:", tx["txid"])
    print("Size:", tx["size"], "bytes")
    print("Weight:", tx["weight"])
    print("Fee:", tx["fee"], "satoshis")
    print("Inputs:", len(tx["vin"]))
    print("Outputs:", len(tx["vout"]))
    print("Confirmed:", tx["status"]["confirmed"])

else:
    print("\n❌ Transaction not found.")
    print("HTTP Status:", response.status_code)