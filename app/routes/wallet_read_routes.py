from app import app
from flask import request, jsonify
import app.utils as utils

from app.repositories import (
    balance_repositories, 
    transaction_repositories,
)

import uuid


# view balance

@app.route('/api/v1/wallet', methods=['GET'])
@utils.authenticate_token
@utils.get_balance_data
def handle_view_balance_request(balance_data):
    return jsonify({
        "status": "success",
        "data": {
            "wallet": {
                "id": balance_data.id,
                "owned_by": balance_data.owned_by,
                "status": balance_data.status,
                "enabled_at": balance_data.enabled_at,
                "balance": balance_data.balance
            }
        }
    }), 200


# view transactions

@app.route('/api/v1/wallet/transactions', methods=['GET'])
@utils.authenticate_token
@utils.get_balance_data
def handle_view_transactions_request(balance_data):
    # transactions retrieval
    cur_transactions = transaction_repositories.Transaction(
        owned_by=balance_data.owned_by
    ).get_transactions_from_customer_xid(balance_data.owned_by)

    # transactions parsing
    cur_transactions_parsed = []
    for t in cur_transactions:
        cur_transactions_parsed.append({
            "id": t.id,
            "status": t.status,
            "transacted_at": t.transacted_at,
            "type": t.type,
            "amount": t.amount,
            "reference_id": t.reference_id
        })

    # generate return
    return jsonify({
        "status": "success",
        "data": {
            "transactions": cur_transactions_parsed
        }
    }), 200