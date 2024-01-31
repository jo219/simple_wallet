from app import app
from flask import request, jsonify

import app.utils as utils

from app.repositories import (
    balance_repositories,
    transaction_repositories,
)

import uuid
from datetime import datetime


# (dis/en)able wallet

@app.route('/api/v1/wallet', methods=['POST', 'PATCH'])
@utils.authenticate_token
def handle_activate_wallet_request(customer_xid):

    # retrieve existing db
    balance_data = balance_repositories.Balance(
        owned_by=customer_xid
    ).get_balance_from_customer_xid(customer_xid)


    # error checking

    error = ''

    if balance_data:
        if (request.method == 'POST') and (balance_data.status == 'enabled'):
            error = 'Already enabled'
        elif (request.method == 'PATCH') and (balance_data.status == 'disabled'):
            error = 'Already disabled'
    else:
        if request.method == 'PATCH':
            error = 'Wallet not found'
    
    if error != '':
        return jsonify({
            "status": "fail",
            "data": {
                "error": error
            }
        }), 400
    
    if balance_data:
        if (request.method == 'POST'):
            balance_data = balance_data.enable_wallet()
        elif (request.method == 'PATCH'):
            is_disabled = request.form.get('is_disabled')
            if not ((is_disabled is not None) and (is_disabled.lower() == 'true')):
                return jsonify({
                    "status": "fail",
                    "data": {
                        "error": "To disable, flag must be provided"
                    }
                }), 400

            balance_data = balance_data.disable_wallet()
    else:
        # initialize balance if record have not exist
        balance_data = balance_repositories.Balance(
            id = str(uuid.uuid4()),
            owned_by = customer_xid,
            status = 'enabled',
            enabled_at = datetime.now(),
            disabled_at = None,
            balance = 0
        )
        balance_data.init_balance()

    wallet_data = {
        "id": balance_data.id,
        "owned_by": balance_data.owned_by,
        "status": balance_data.status,
        "balance": balance_data.balance
    }

    if (request.method == 'POST'):
        wallet_data["enabled_at"] = balance_data.enabled_at
    elif (request.method == 'PATCH'):
        wallet_data["disabled_at"] = balance_data.disabled_at

    response_data = {
        "status": "success",
        "data": {
            "wallet": wallet_data
        }
    }

    return jsonify(response_data), 201
        

# cash-flowing util
def cashf_sanitize_request_body(reference_id, amount):
    error = ''
    amount_int = 0
    if (not reference_id) or (reference_id is None) or (reference_id.strip() == '') or transaction_repositories.is_reference_id_exist(reference_id):
        error = 'invalid reference_id'
    elif (not amount) or (amount is None) or (not amount.isdigit()):
        error = 'invalid amount data format'
    else:
        amount_int = int(amount)
        if amount_int < 0: 
            error = 'amount must more than 0'

    return reference_id, amount_int, error


# deposits

@app.route('/api/v1/wallet/deposits', methods=['POST'])
@utils.authenticate_token
@utils.get_balance_data
def handle_deposits_wallet_request(balance_data):

    # error checking
    reference_id, amount_int, error = cashf_sanitize_request_body(
        request.form.get('reference_id'), 
        request.form.get('amount'),
    )
    if error != '':
        return jsonify({
            "status": "fail",
            "data": {
                "error": error
            }
        }), 400

    cur_status = 'success'
    # update balance
    try:
        balance_data.update_balance_amount(balance_data.balance + amount_int)
    except:
        cur_status = 'fail'

    # insert transaction
    tr_obj = transaction_repositories.Transaction(
        id = str(uuid.uuid4()), 
        owned_by = balance_data.owned_by, 
        status = cur_status, 
        transacted_at = datetime.now(), 
        t_type = 'deposit', 
        amount = amount_int, 
        reference_id = reference_id
    ).create_transaction()

    tr_data = {
      "id": tr_obj.id,
      "status": tr_obj.status,
      "amount": tr_obj.amount,
      "reference_id": tr_obj.reference_id
    }

    tr_data["deposited_by"] = tr_obj.owned_by
    tr_data["deposited_at"] = tr_obj.transacted_at

    return jsonify({
        "status": "success",
        "deposit": tr_data
    }), 200


# withdrawals

@app.route('/api/v1/wallet/withdrawals', methods=['POST'])
@utils.authenticate_token
@utils.get_balance_data
def handle_withdrawals_wallet_request(balance_data):

    # error checking
    reference_id, amount_int, error = cashf_sanitize_request_body(
        request.form.get('reference_id'), 
        request.form.get('amount'),
    )
    if amount_int > balance_data.balance: error = 'balance insufficient'
    if error != '':
        return jsonify({
            "status": "fail",
            "data": {
                "error": error
            }
        }), 400

    cur_status = 'success'
    # update balance
    try:
        balance_data.update_balance_amount(balance_data.balance - amount_int)
    except:
        cur_status = 'fail'

    # insert transaction
    tr_obj = transaction_repositories.Transaction(
        id = str(uuid.uuid4()), 
        owned_by = balance_data.owned_by, 
        status = cur_status, 
        transacted_at = datetime.now(), 
        t_type = 'withdrawal', 
        amount = amount_int, 
        reference_id = reference_id
    ).create_transaction()

    tr_data = {
      "id": tr_obj.id,
      "status": tr_obj.status,
      "amount": tr_obj.amount,
      "reference_id": tr_obj.reference_id
    }

    tr_data["withdrawn_by"] = tr_obj.owned_by
    tr_data["withdrawn_at"] = tr_obj.transacted_at

    return jsonify({
        "status": "success",
        "withdrawal": tr_data
    }), 200