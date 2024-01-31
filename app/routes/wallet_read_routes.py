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
def handle_view_balance_request(customer_xid):

    balance_data = balance_repositories.Balance(
        owned_by=customer_xid
    ).get_balance_from_customer_xid(customer_xid)
    
    if (not balance_data) or (balance_data.status != 'enabled'):
        response_data = {
            "status": "fail",
            "data": {
                "error": "Wallet disabled"
            }
        }    
        return jsonify(response_data), 400

    # Generate the response data
    response_data = {
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
    }

    return jsonify(response_data), 200


# view transactions

@app.route('/api/v1/wallet/transactions', methods=['GET'])
@utils.authenticate_token
def handle_view_transactions_request(customer_xid):

    balance_data = balance_repositories.Balance(
        owned_by=customer_xid
    ).get_balance_from_customer_xid(customer_xid)
    
    if (not balance_data) or (balance_data.status != 'enabled'):
        response_data = {
            "status": "fail",
            "data": {
                "error": "Wallet disabled"
            }
        }    
        return jsonify(response_data), 400

    # transactions retrieval
    cur_transactions = transaction_repositories.Transaction(
        owned_by=customer_xid
    ).get_transactions_from_customer_xid(customer_xid)

    # Generate the response data
    response_data = {
        "status": "success",
        "data": {
            "transactions": cur_transactions
        }
    }

    '''
    "transactions": [
      {
        "id": "7ae5aa7b-821f-4559-874b-07eea5f47962",
        "status": "success",
        "transacted_at": "1994-11-05T08:15:30-05:00",
        "type": "deposit",
        "amount": 14000,
        "reference_id": "305247dc-6081-409c-b418-e9d65dee7a94"
      },
    '''

    return jsonify(response_data), 200