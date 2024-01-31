import os, sqlite3

def remove_existing_db():
    print("try to remove existing sqlite database...")
    file_path = './database.db'
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"file '{file_path}' removed successfully.")
    else:
        print(f"file '{file_path}' does not exist.")

def create_table():
    print("initiate new sqlite database...")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # create tables

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            token TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE balances (
            id TEXT PRIMARY KEY,
            owned_by TEXT,
            status TEXT,
            enabled_at TIMESTAMP,
            balance INTEGER, 
            FOREIGN KEY (owned_by) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE transactions (
            id TEXT PRIMARY KEY,
            status TEXT,
            transacted_at TIMESTAMP,
            type TEXT,
            amount INTEGER,
            reference_id TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("\nnew sqlite database successfully initialized!")

if __name__ == '__main__':
    remove_existing_db()
    create_table()
