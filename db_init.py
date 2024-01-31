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
            owned_by TEXT NOT NULL,
            status TEXT CHECK (status IN ('enabled', 'disabled')),
            enabled_at TIMESTAMP,
            disabled_at TIMESTAMP,
            balance INTEGER, 
            FOREIGN KEY (owned_by) REFERENCES users (id),
            UNIQUE(owned_by)
        )
    ''')

    cursor.execute('''
        CREATE TABLE transactions (
            id TEXT PRIMARY KEY,
            owned_by TEXT NOT NULL,
            status TEXT,
            transacted_at TIMESTAMP,
            type TEXT CHECK (status IN ('withdrawal', 'deposit')),
            amount INTEGER,
            reference_id TEXT,
            FOREIGN KEY (owned_by) REFERENCES users (id),
            UNIQUE(owned_by)
        )
    ''')

    conn.commit()
    conn.close()
    print("\nnew sqlite database successfully initialized!")

if __name__ == '__main__':
    remove_existing_db()
    create_table()
