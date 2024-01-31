import sqlite3

def get_wallet_from_customer_xid(customer_xid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO users (id, token) 
        VALUES (?, ?)
    ''', (id, token))

    conn.commit()
    conn.close()

def get_id_from_token(token):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE token=?", (token,))
    result = cursor.fetchone()

    if result:
        customer_xid = result[0]
        return True, customer_xid
    else:
        return False, None
