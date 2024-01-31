import sqlite3
import uuid

from datetime import datetime


class Balance:
    def __init__(self, id=None, owned_by=None, status='enabled', enabled_at=None, disabled_at=None, balance=0):
        self.id = id
        self.owned_by = owned_by
        self.status = status
        self.enabled_at = enabled_at
        self.disabled_at = disabled_at
        self.balance = balance

    def init_balance(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO balances (id, owned_by, status, enabled_at, disabled_at, balance) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            str(self.id),
            self.owned_by,
            self.status,
            self.enabled_at,
            self.disabled_at,
            self.balance
        ))

        conn.commit()
        conn.close()
    
    def enable_wallet(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        self.status = 'enabled'
        self.enabled_at = datetime.now()

        cursor.execute('''
            UPDATE balances 
            SET status = ?,
                enabled_at = ?
            WHERE id = ?;
        ''', (self.status, self.enabled_at, self.id))

        conn.commit()
        conn.close()
        return self

    def disable_wallet(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        self.status = 'disabled'
        self.disabled_at = datetime.now()

        cursor.execute('''
            UPDATE balances 
            SET status = ?,
                disabled_at = ?
            WHERE id = ?;
        ''', (self.status, self.disabled_at, self.id))

        conn.commit()
        conn.close()
        return self

    @classmethod
    def get_balance_from_customer_xid(cls, customer_xid):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM balances WHERE owned_by=?", (customer_xid,))
        balance_data = cursor.fetchone()
        conn.close()

        if balance_data:
            return cls(*balance_data)
        return None
