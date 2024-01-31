from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/v1/init', methods=['POST'])
def handle_init_request():
    if request.form:
        customer_xid = request.form.get('customer_xid')

        token = "cb04f9f26632ad602f14acef21c58f58f6fe5fb55a"

        response_data = {
            "data": {
                "token": token
            },
            "status": "success"
        }

        return jsonify(response_data), 200
    else:
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


if __name__ == '__main__':
    app.run(debug=True)
