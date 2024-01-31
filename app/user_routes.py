from app import app
from flask import request, jsonify

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
    token = "cb04f9f26632ad602f14acef21c58f58f6fe5fb55b"
    response_data = {
        "data": {
            "token": token
        },
        "status": "success"
    }

    return jsonify(response_data), 200
        
