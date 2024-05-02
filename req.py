import requests
import json

url = 'http://127.0.0.1:5000/api/send_transaction'

data = {
    'contract_name': 'disbursement',
    'function_name': 'startDisbursement',
    'user_address': '0xf18b30CE11317de6177fD6dE9a1e101A8B46986E',
    'encrypted_private_key': 'iEtLPC1tdEV6PfX53l/qQftvzuoUqG8sjAZUFWRhjOc18FRNc/x7Iw',
    'value': 0.1
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    print("Transaction sent successfully.")
    print("Transaction Hash:", response.json().get('txn_hash'))
else:
    print("Failed to send transaction.")
    print("Error:", response.text)
