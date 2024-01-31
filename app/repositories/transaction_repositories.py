import sqlite3
import uuid

from datetime import datetime


def is_reference_id_exist(ref_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM transactions WHERE reference_id = ?)", (ref_id,))
    result = cursor.fetchone()[0]

    conn.close()

    return result == 1


class Transaction:
    def __init__(self, id=None, owned_by=None, status='success', transacted_at=None, t_type='deposit', amount=0, reference_id=None):
        self.id = id
        self.owned_by = owned_by
        self.status = status
        self.transacted_at = transacted_at
        self.type = t_type
        self.amount = amount
        self.reference_id = reference_id

    def create_transaction(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        print("self.type")
        print(self.type)

        cursor.execute('''
            INSERT INTO transactions (id, owned_by, status, transacted_at, type, amount, reference_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(self.id),
            self.owned_by,
            self.status,
            self.transacted_at,
            self.type,
            self.amount,
            self.reference_id,
        ))

        conn.commit()
        conn.close()
        return self

    @classmethod
    def get_transactions_from_customer_xid(cls, customer_xid):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions WHERE owned_by=?", (customer_xid,))
        cur_transactions = cursor.fetchall()
        conn.close()

        transactions = []
        for row in cur_transactions:
            transactions.append(cls(*row))
        
        return transactions
