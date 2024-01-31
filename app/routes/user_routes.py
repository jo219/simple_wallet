from app import app
from flask import request, jsonify

import app.utils as utils
from app.repositories import user_repositories

@app.route('/api/v1/init', methods=['POST'])
def handle_init_request():
    # error handling
    customer_xid = request.form.get('customer_xid')
    if not customer_xid:
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

    return jsonify(response_data), 200
        
