from app import app
from flask import request, jsonify

import app.utils as utils
from app.repositories import (
    user_repositories,
    transaction_repositories,
)

import uuid


@app.route('/api/v1/init', methods=['POST'])
def handle_init_request():
    # error handling
    customer_xid = request.form.get('customer_xid')
    if (not customer_xid) or (customer_xid.strip() == ''):
        error_response = {
            "data": {
                "error": {
                    "customer_xid": [
                        "Missing data for required field."
                    ]
                }
            },
            "status": "fail"
        }
        return jsonify(error_response), 400

    # logic start
    token = utils.generate_random_string(42)
    user_repositories.store_session_token(customer_xid, token)

    response_data = {
        "data": {
            "token": token
        },
        "status": "success"
    }

    return jsonify(response_data), 201
        
@app.route('/api/v1/reference-id', methods=['GET'])
def handle_generate_reference_id_request():
    
    reference_id = str(uuid.uuid4())
    while transaction_repositories.is_reference_id_exist(reference_id):
        reference_id = str(uuid.uuid4())

    response_data = {
        "data": {
            "reference_id": reference_id
        },
        "status": "success"
    }

    return jsonify(response_data), 201