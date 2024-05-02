from main import get_loan_status as main_get_loan_status, get_balance as main_get_balance, get_transaction_status as main_get_transaction_status

def get_transaction_status(user_id):
    #add error handling, logging, or data transformation here if needed
    return main_get_transaction_status(user_id)

def get_loan_status(user_id):
    # additional processing or different arguments can be handled here
    return main_get_loan_status('loan', user_id)

def get_balance_status(user_id):
    # interface function can simplify or modify the call
    return main_get_balance('balance', user_id)
