import sqlite3

def store_session_token(id, token):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO users (id, token) 
        VALUES (?, ?)
    ''', (id, token))

    conn.commit()
    conn.close()