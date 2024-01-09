import sqlite3 as lite
import tkinter as tk
from tkinter import messagebox
import pandas as pd

combo_category_expenses = None
some_updated_value = None
tree_category = None

def update_category_options(tree_category):
    categories = see_category()
    combo_category_expenses['values'] = ()
    combo_category_expenses['values'] = [category[1] for category in categories]
    tree_category = some_updated_value

def update_expense_options(tree_category):
    categories = see_category()
    update_expense_options(combo_category_expenses['values'])

def update_income_options(tree_category):
    categories = see_category()
    update_income_options(combo_category_expenses['values'])

con = lite.connect('dados.db')

def insert_category(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Category (name) VALUES (?)"
        cur.execute(query, i)


def insert_incomes(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Incomes (category, adding_in,value) VALUES (?, ?, ?)"
        cur.execute(query, i)


def insert_expenses(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Expenses (category, withdrawal_in,value) VALUES (?, ?, ?)"
        cur.execute(query, i)

def delete_incomes(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Incomes WHERE id=?"
        cur.execute(query, i)


def delete_expenses(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Expenses WHERE id=?"
        cur.execute(query, i)
        
def delete_category(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Category Where id=?"
        cur.execute(query, i)
        
def delete_category_selected():
    selected_category = tree_category.focus()
    if selected_category:
        category_id = tree_category.item(selected_category, 'values')[0]
        delete_category([category_id])
        messagebox.showinfo('Done', 'Category deleted successfully!')
        update_category_options()
        update_expense_options()
        update_income_options()

def see_category():
    list_items = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Category")
        rows = cur.fetchall()
        for row in rows:
            list_items.append(row)
            
    return list_items

print(see_category())


def see_incomes():
    list_items = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Incomes")
        rows = cur.fetchall()
        for row in rows:
            list_items.append(row)
    
    return list_items


def see_expenses():
    list_items = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Expenses")
        rows = cur.fetchall()
        for row in rows:
            list_items.append(row)
    
    return list_items

def chart():
    expenses = see_expenses()
    incomes = see_incomes()
    
    chart_list = []
    
    for i in expenses:
        chart_list.append(i)
    for i in incomes:
        chart_list.append(i)
    
    return chart_list

def values_bar():
    incomes = see_incomes()
    incomes_list = []
    
    for i in incomes:
        incomes_list.append(i[3])
        
    total_incomes = sum(incomes_list)
    
    expenses = see_expenses()
    expenses_list = []
    
    for i in expenses:
        expenses_list.append(i[3])
        
    total_expenses = sum(expenses_list)
    
    total_balance = total_incomes - total_expenses
    
    return[total_incomes, total_expenses, total_balance]

def pie_values():
    expenses = see_expenses()
    incomes = see_incomes()
    
    list_chart = []
    
    for i in expenses:
        list_chart.append(i)
    for i in incomes:
        list_chart.append(i)
    
    dataframe = pd.DataFrame(list_chart,columns=['Id', 'Category', 'Date', 'Value'])
    dataframe = dataframe.groupby('Category')['Value'].sum()
    
    list_quant = dataframe.values.tolist()
    list_categories = []
    
    for i in dataframe.index:
        list_categories.append(i)
    
    return [list_categories, list_quant]



def main():
    con = lite.connect('dados.db')

    combo_category_expenses = None
    some_updated_value = None
    
    category_options = see_category()
    expense_options = see_expenses()
    income_options = see_incomes()
    
    con.close()

if __name__ == "__main__":
    main()
