import requests

url = "https://mempool.space/api/mempool/recent"

response = requests.get(url, timeout=10)

if response.status_code == 200:

    transactions = response.json()

    print("=== LIVE BITCOIN TRANSACTIONS ===")
    print()

    for i, tx in enumerate(transactions, start=1):
        print(f"Transaction {i}")
        print("TXID:", tx["txid"])
        print("Fee:", tx["fee"], "satoshis")
        print("Size:", tx["vsize"], "vbytes")
        print("Value:", tx["value"], "satoshis")
        print("-" * 50)

else:
    print("Unable to retrieve live transactions.")
    print("Status code:", response.status_code)