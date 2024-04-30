import json
from web3 import Web3
from pipeline import blockchain_connection
import dict2
from dict2 import abi_paths, contract_addresses, private_key

def load_contract(abi_path, contract_addresses):
    web3 = blockchain_connection()
    if not web3 or not web3.is_connected():
        print("Failed to connect to the Ethereum network.")
        return None
    
    try:
        with open(abi_path, 'r') as file:
            abi = json.load(file)
    except FileNotFoundError:
        print(f"ABI file at {abi_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding ABI file at {abi_path}. Ensure it is valid JSON.")
        return None

    return web3.eth.contract(address=Web3.to_checksum_address(contract_addresses), abi=abi)

# Load contracts
contracts = {name: load_contract(abi_path, contract_addresses[name]) for name, abi_path in dict2.abi_paths.items()}

# interact with contract
def get_loan_status(contract_name, user_address):
    contract = contracts.get(contract_name)
    if contract:
        try:
            # Corrected the call to the contract's function
            return contract.functions.getLoanStatus(user_address).call()
        except Exception as e:
            print(f"Failed to retrieve loan status: {e}")
    else:
        return f"{contract_name} Contract is not available."

# disburse funds from lender to borrower
def disburse_funds(lender_address, borrower_address, amount):
    disbursement_contract = contracts.get('disbursement')
    if disbursement_contract:
        try:
            txn_dict = {
                'from': lender_address,
                'gas': 2000000,
            }
            txn = disbursement_contract.functions.disburseFunds(borrower_address, Web3.toWei(amount, 'ether')).buildTransaction(txn_dict)

            return "Disbursement transaction prepared."
        except Exception as e:
            print(f"Failed to disburse funds: {e}")
    else:
        return "Disbursement contract is not available."

# calculate interest based on loan terms
def interest_calculation(loan_id):
    interest_calculation_contract = contracts.get('interest_calculation')
    if interest_calculation_contract:
        try:
            interest_amount = interest_calculation_contract.functions.calculateInterest(loan_id).call()
            return interest_amount
        except Exception as e:
            print(f"Failed to calculate interest: {e}")
    else:
        return "Interest calculation contract is not available."

# create loan agreement
def loan_agreement(loan_terms):
    loan_agreement_contract = contracts.get('loan_agreement')
    if loan_agreement_contract:
        try:
            txn = loan_agreement_contract.functions.createLoanAgreement(**loan_terms).buildTransaction({
                'from': loan_terms['lender_address'],
                'gas': 2000000,
            })
            
            return "Loan agreement transaction prepared."
        except Exception as e:
            print(f"Failed to create loan agreement: {e}")
    else:
        return "Loan agreement contract is not available."

# loan repayment to borrower
def repayment_calculation(borrower_address, loan_id, amount):
    repayment_contract = contracts.get('repayment')
    if repayment_contract:
        try:
            txn_dict = {
                'from': borrower_address,
                'gas': 2000000,
            }
            txn = repayment_contract.functions.submitPayment(loan_id, Web3.toWei(amount, 'ether')).buildTransaction(txn_dict)
            
            return "Repayment transaction prepared."
        except Exception as e:
            print(f"Failed to submit repayment: {e}")
    else:
        return "Repayment contract is not available."

# send transaction
def send_transaction(contract_function, user_address, private_key, value=0):
    web3 = blockchain_connection()
    if not web3 or not web3.isConnected():
        print("Failed to connect to the Ethereum network.")
        return None
    
    try:
        txn_dict = {
            'from': user_address,
            'value': Web3.toWei(value, 'ether'),
            'gas': 2000000,
            'nonce': web3.eth.getTransactionCount(user_address)
        }
        txn = contract_function.buildTransaction(txn_dict)
        signed_txn = web3.eth.account.signTransaction(txn, private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return web3.toHex(txn_hash)
    except Exception as e:
        print(f"Failed to send transaction: {e}")
    return "Failed to send transaction."

