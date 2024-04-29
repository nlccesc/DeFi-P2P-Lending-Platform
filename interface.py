from dict import example_data

def get_transaction_status(user_id):
    return example_data.get('transactions', {}).get(user_id, [])

def get_loan_status(user_id):
    return example_data.get('loans', {}).get(user_id, [])

def get_balance_status(user_id):
    return example_data.get('balances', {}).get(user_id, [])

