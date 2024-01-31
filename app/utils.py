import secrets
import string

from functools import wraps
from flask import request, jsonify

from app.repositories import (
    user_repositories,
    balance_repositories,
)

def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# middleware function to check authentication

def authenticate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({"status": "error", "message": "Authorization header missing"}), 401

        provided_token = request.headers.get('Authorization').split()[-1]
        is_token_valid, customer_xid = user_repositories.get_id_from_token(provided_token)

        if not is_token_valid:
            return jsonify({
                "data": {
                    "error": {
                        "token": [
                            "Token missing or invalid"
                        ]
                    }
                },
                "status": "fail"
            }), 401

        return func(customer_xid, *args, **kwargs)
    return wrapper


# middleware to get balance data
def get_balance_data(func):
    @wraps(func)
    def wrapper(customer_xid, *args, **kwargs):
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

        return func(balance_data, *args, **kwargs)
    return wrapper


# middleware to access db

# def with_db(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()

#         # Call the decorated function with the database cursor
#         result = func(cursor, *args, **kwargs)

#         conn.commit()
#         conn.close()

#         return result

#     return wrapper