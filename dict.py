example_data = {
    "transactions": {
        "user1": [{"date": "2023-04-28", "amount": 150, "type": "deposit"},
                  {"date": "2023-04-29", "amount": 75, "type": "withdrawal"}],
        "user2": [{"date": "2023-04-27", "amount": 200, "type": "deposit"}]
    },
    "loans": {
        "user1": {"status": "current", "due_date": "2023-12-15", "amount_due": 1000},
        "user2": {"status": "paid", "due_date": "2022-12-15", "amount_due": 0}
    },
    "balances": {
        "user1": 2300,
        "user2": 4580
    }
}