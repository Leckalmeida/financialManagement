import sqlite3 as lite

def create_tables():
    con = lite.connect('dados.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Category(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS Incomes(id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, adding_in DATE, value DECIMAL)")
        cur.execute("CREATE TABLE IF NOT EXISTS Expenses(id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, withdrawal_in DATE, value DECIMAL)")

create_tables()