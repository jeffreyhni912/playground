import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('db\\scripts_database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM scripts')
        print(c.description)
        all_rows = c.fetchall()
        print(all_rows)