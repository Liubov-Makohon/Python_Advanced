import sqlite3


def execute_query(query, args=()):
    with sqlite3.connect('chinook.db') as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        records = cur.fetchall()
    return records

