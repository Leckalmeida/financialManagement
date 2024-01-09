from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox

from PIL import Image, ImageTk

from tkinter.ttk import Progressbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from tkcalendar import Calendar, DateEntry
from datetime import date

from view import *

co0 = "#2e2d2b"
co1 = "#feffff"
co2 = "#4fa882"
co3 = "#38576b"
co4 = "#403d3d"
co5 = "#e06636"
co6 = "#038cfc"
co7 = "#3fbfb9"
co8 = "#263238"
co9 = "#e9edf5"

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

window = Tk()
window.title('Financial Tracking Sheet')
window.geometry('1024x768')
window.configure(background=co9)
window.resizable(width=FALSE, height=FALSE)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

style = ttk.Style(window)
style.theme_use("alt")

frameUp = Frame(window, width=1180, height=80, bg=co1, relief="flat")
frameUp.grid(row=0, column=0, sticky='ew')

frameMiddle = Frame(window, width=1180, height=400, bg=co1, pady=20, relief="raised")
frameMiddle.grid(row=1, column=0, pady=1, padx=0, sticky='nsew')

frameDown = Frame(window, width=1180, height=320, bg=co1, relief="flat")
frameDown.grid(row=2, column=0, pady=0, padx=0, sticky='ew')


app_img = Image.open('images/logo.png')
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)


app_logo = Label(frameUp, image=app_img, text=" Personal Financial Tracker", width=1050,height=75,compound=LEFT,
                 padx=5,relief=RAISED,anchor=NW,font=("Arial 20 bold"),bg=co1, fg=co4)
app_logo.place(x=0, y=0)

global tree

def update_category_options():
    categories = see_category()
    combo_category_expenses['values'] = ()
    combo_category_expenses['values'] = [category[1] for category in categories]

def update_expense_options():
    categories = see_category()
    update_expense_options(combo_category_expenses['values'])

def update_income_options():
    categories = see_category()
    update_income_options(combo_category_expenses['values'])

def update_graphic_bar():
    graphic_bar()

def insert_categories_b():
    name = e_category.get()
    list_insert = [name]
    for i in list_insert:
        if i == '':
            messagebox.showerror('Error', 'Fill all the blanks')
            return
        
    insert_category(list_insert)
    messagebox.showinfo('Done!', 'The data has been successfully inserted!')
    
    e_category.delete(0,'end')
    
    categories_function = see_category()
    category = []
    update_category_options()
    
    for i in category_function:
        category.append(i[1])
    combo_category_expenses['values'] = (category)
    update_table()
    show_incomes()
    
def insert_incomes_b():
    name = 'Incomes'
    date = e_cal_incomes.get()
    amount = e_value_incomes.get()
    
    list_insert = [name, date, amount]
    
    for i in list_insert:
        if i == '':
            messagebox.showerror('Error', 'Fill all the blanks')
            return
        
    insert_incomes(list_insert)
    messagebox.showinfo('Done!', 'The data has been successfully inserted!')
    e_cal_incomes.delete(0,'end')
    e_value_incomes.delete(0,'end')
    update_table()
    show_incomes()
    graphic_bar()


def insert_expenses_b():
    name = combo_category_expenses.get()
    date = entry_cal_expense.get()
    amount = e_value_expenses.get()
    
    list_insert = [name, date, amount]
    
    for i in list_insert:
        if i == '':
            messagebox.showerror('Error', 'Fill all the blanks')
            return
        
    insert_expenses(list_insert)
    messagebox.showinfo('Done!', 'The data has been successfully inserted!')
    combo_category_expenses.delete(0,'end')
    entry_cal_expense.delete(0,'end')
    e_value_expenses.delete(0,'end')
    update_table()
    show_incomes()
    update_summary_and_pie_chart()

def delete_data():
    try:
        treev_data = tree.focus()
        treev_dict = tree.item(treev_data)
        treev_list = treev_dict['values']
        value = treev_list[0]
        name = treev_list[1]
        
        if name in ['Incomes', 'Income']:
            delete_incomes([value])
            messagebox.showinfo('Done', 'Deleted!')
            
            show_incomes()
            percentage()
            graphic_bar()
            pie_chart()
            summary()
            
        else:
            delete_expenses([value])
            messagebox.showinfo('Done', 'Deleted!')
            show_incomes()
            percentage()
            graphic_bar()
            pie_chart()
            summary()

    except IndexError:
        messagebox.showerror('Error', 'You need to select one of the options')
    show_incomes()
    update_summary_and_pie_chart()


tree_category = None

def delete_category_b():
    try:
        treev_data = tree_category.focus()
        if treev_data:
            treev_dict = tree_category.item(treev_data)
            treev_list = treev_dict['values']
            value = treev_list[0]
            
            confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete category ID {value}?")
            
            if confirmation:
                delete_category([value])
                messagebox.showinfo('Done', 'Category deleted successfully!')
        else:
            messagebox.showerror('Error', 'You need to select a category to delete')
    except IndexError:
        messagebox.showerror('Error', 'An error occurred while deleting the category')
    update_summary_and_pie_chart()

def update_progress_bar(bar, spending_commitment):
    bar['value'] = spending_commitment
    frameMiddle.after(1000, percentage)

def percentage():
    total_incomes, total_expenses, total_balance = values_bar()
    
    if total_incomes != 0:
        spending_commitment = (total_expenses / total_incomes) * 100
    else:
        spending_commitment = 0
        
    l_name = Label(frameMiddle, text="Spending Commitment",height=1,anchor=NW,font=("Arial 12"), bg=co1, fg=co4)
    l_name.place(x=7, y=5)
    
    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=15)
    bar = Progressbar(frameMiddle, length=180,style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = spending_commitment
    
    if total_incomes != 0:
        value = (total_expenses / total_incomes) * 100
    else:
        value = 0
        
    l_percentage = Label(frameMiddle, text="{:,.2f}%".format(value),anchor=NW,font=("Arial 12"), bg=co1, fg=co4)
    l_percentage.place(x=200, y=35)
    update_progress_bar(bar, spending_commitment)


figure = plt.Figure(figsize=(4, 3.45), dpi=60)
ax = figure.add_subplot(111)
ax.autoscale(enable=True, axis='both', tight=None)

def graphic_bar():
    list_categories = ['Incomes', 'Expenses', 'Balance']
    list_values = values_bar()

    ax.clear()

    ax.bar(list_categories, list_values, color=colors, width=0.9)

    c = 0
    for i in ax.patches:
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(list_values[c])),fontsize=17,fontstyle='italic',verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(list_categories,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figure, frameMiddle)
    canva.get_tk_widget().place(x=10, y=70)

global l_summary_income, l_summary_expense, l_summary_balance

def summary():
    values = values_bar()

    l_summary_income.config(text="US$ {:,.2f}".format(values[0]))
    l_summary_expense.config(text="US$ {:,.2f}".format(values[1]))
    l_summary_balance.config(text="US$ {:,.2f}".format(values[2]))
    update_graphic_bar()

    l_line = Label(frameMiddle, text="", width=215, height=1, anchor=NW, font=('Verdana 1'), bg='#545454')
    l_line.place(x=309, y=52)
    l_summary = Label(frameMiddle, text="Total  Monthly  Incomes      ".upper(), anchor=NW, font=('Arial 12'), bg=co1, fg='#83a9e6')
    l_summary.place(x=309, y=35)
    l_summary = Label(frameMiddle, text="US$ {:,.2f}".format(values[0]), anchor=NW, font=('Verdana 17'), bg=co1, fg='#545454')
    l_summary.place(x=309, y=70)

    l_line = Label(frameMiddle, text="", width=215, height=1, anchor=NW, font=('Verdana 1'), bg='#545454')
    l_line.place(x=309, y=132)
    l_summary = Label(frameMiddle, text="Total  Monthly  Expenses   ".upper(), anchor=NW, font=('Arial 12'), bg=co1, fg='#83a9e6')
    l_summary.place(x=309, y=115)
    l_summary = Label(frameMiddle, text="US$ {:,.2f}".format(values[1]), anchor=NW, font=('Verdana 17'), bg=co1, fg='#545454')
    l_summary.place(x=309, y=150)

    l_line = Label(frameMiddle, text="", width=215, height=1, anchor=NW, font=('Verdana 1'), bg='#545454')
    l_line.place(x=309, y=207)
    l_summary = Label(frameMiddle, text="Total  Monthly  Balance      ".upper(), anchor=NW, font=('Arial 12'), bg=co1, fg='#83a9e6')
    l_summary.place(x=309, y=190)
    l_summary = Label(frameMiddle, text="US$ {:,.2f}".format(values[2]), anchor=NW, font=('Verdana 17'), bg=co1, fg='#545454')
    l_summary.place(x=309, y=220)
    


l_summary_income = Label(frameMiddle, text="", anchor=NW, font=('Verdana 17'), bg=co1, fg='#545454')
l_summary_income.place(x=309, y=70)

l_summary_expense = Label(frameMiddle, text="", anchor=NW, font=('Verdana 17'), bg=co1, fg='#545454')
l_summary_expense.place(x=309, y=150)

l_summary_balance = Label(frameMiddle, text="", anchor=NW, font=('Verdana 17'), bg=co1, fg='#545454')
l_summary_balance.place(x=309, y=220)

frame_pie_chart = Frame(frameMiddle,width=520,height=270,bg=co2)
frame_pie_chart.place(x=450, y=5)


def pie_chart():
    figure = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figure.add_subplot(111)

    list_values = pie_values()[1]
    list_categories = pie_values()[0]

    explode = []
    for i in list_categories:
        explode.append(0.05)

    ax.pie(
        list_values,
        explode=explode,
        wedgeprops=dict(width=0.4),
        autopct='%1.1f%%',
        colors=colors,
        shadow=True,
        startangle=90
    )
    ax.legend(list_categories, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_category = FigureCanvasTkAgg(figure, frame_pie_chart)
    canva_category.get_tk_widget().grid(row=0, column=0)
    
    
figure_pie = plt.Figure(figsize=(5, 3), dpi=90)

def update_pie_chart():
    global figure_pie
    figure_pie.clf()
    pie_chart()

update_pie_chart()


def update_summary_and_pie_chart():
    summary()
    update_pie_chart()


percentage()
graphic_bar()
pie_chart()
summary()


frame_income = Frame(frameDown, width=300, height=250, bg=co1)
frame_income.grid(row=0, column=0)

frame_operations = Frame(frameDown, width=220, height=250, bg=co1)
frame_operations.grid(row=0, column=1,padx=5)

frame_settings = Frame(frameDown, width=220, height=250, bg=co1)
frame_settings.grid(row=0, column=2,padx=5)

app_chart = Label(frameMiddle,text="Income and Expense Chart",anchor=NW,font=("Arial 12 bold"),bg=co1, fg=co4)
app_chart.place(x=12, y=390)

def show_incomes():
    chart_head = ['#Id','Category','Date','Amount']

    list_items = chart()
    
    global tree

    tree = ttk.Treeview(frame_income, selectmode="extended",columns=chart_head, show="headings")
    vsb = ttk.Scrollbar(frame_income, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_income, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in chart_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n],anchor=hd[n])
        n+=1

    for item in list_items:
        tree.insert('', 'end', values=item)
        
def update_table():
    items = tree.get_children()
    for item in items:
        tree.delete(item)
    show_incomes()

show_incomes()


l_info = Label(frame_operations, text='Register new expenses',height=1,anchor=NW,font=('Arial 10 bold'),bg=co1,fg=co4)
l_info.place(x=10, y=10)

l_category = Label(frame_operations, text='Category',height=1,anchor=NW,font=('Ivy 10'),bg=co1,fg=co4)
l_category.place(x=10, y=40)

category_function = see_category()
category = []

for i in category_function:
    category.append(i[1])
    
combo_category_expenses = ttk.Combobox(frame_operations,width=10,font=('Ivy 10'))
combo_category_expenses['values'] = (category)
combo_category_expenses.place(x=110, y=41)

l_cal_expenses = Label(frame_operations, text='Date',height=1,anchor=NW,font=('Ivy 10'),bg=co1,fg=co4)
l_cal_expenses.place(x=10, y=70)

entry_cal_expense = DateEntry(frame_operations,width=12,background='darkblue',foreground='white',borderwidth=2,year=2022)
entry_cal_expense.place(x=110, y=71)

l_value_expenses = Label(frame_operations, text='Total Amount',height=1,anchor=NW,font=('Ivy 10'),bg=co1,fg=co4)
l_value_expenses.place(x=10, y=100)
e_value_expenses = Entry(frame_operations, width=14, justify='left',relief='solid')
e_value_expenses.place(x=110, y=101)

img_add_expenses = Image.open('images/add.png')
img_add_expenses = img_add_expenses.resize((17, 17))
img_add_expenses = ImageTk.PhotoImage(img_add_expenses)
insert_expense_button = Button(frame_operations,command=insert_expenses_b, image=img_add_expenses, text=" Add", width=80,compound=LEFT,
                 anchor=NW,font=("Ivy 7 bold"),bg=co1,fg=co0,overrelief=RIDGE)
insert_expense_button.place(x=110, y=131)


l_delete = Label(frame_operations, text='Delete',height=1,anchor=NW,font=('Ivy 10 bold'),bg=co1,fg=co4)
l_delete.place(x=10, y=190)

img_delete = Image.open('images/delete.png')
img_delete = img_delete.resize((17, 17))
img_delete = ImageTk.PhotoImage(img_delete)
delete_button = Button(frame_operations,command=delete_data,image=img_delete, text=" Delete", width=80,compound=LEFT,
                 anchor=NW,font=("Ivy 7 bold"),bg=co1,fg=co0,overrelief=RIDGE)
delete_button.place(x=110, y=190)

l_info = Label(frame_settings, text='Register new incomes',height=1,anchor=NW,font=('Arial 10 bold'),bg=co1,fg=co4)
l_info.place(x=10, y=10)

l_cal_incomes = Label(frame_settings, text='Date',height=1,anchor=NW,font=('Ivy 10'),bg=co1,fg=co4)
l_cal_incomes.place(x=10, y=40)
e_cal_incomes = DateEntry(frame_settings, width=14, justify='left',relief='solid')
e_cal_incomes.place(x=110, y=41)

l_value_incomes = Label(frame_settings, text='Total Amount',height=1,anchor=NW,font=('Ivy 10'),bg=co1,fg=co4)
l_value_incomes.place(x=10, y=70)
e_value_incomes = Entry(frame_settings, width=14, justify='left',relief='solid')
e_value_incomes.place(x=110, y=71)

img_add_incomes = Image.open('images/add.png')
img_add_incomes = img_add_incomes.resize((17, 17))
img_add_incomes = ImageTk.PhotoImage(img_add_incomes)
insert_incomes_button = Button(frame_settings,command=insert_incomes_b,image=img_add_incomes, text=" Add", width=80,compound=LEFT,
                 anchor=NW,font=("Ivy 7 bold"),bg=co1,fg=co0,overrelief=RIDGE)
insert_incomes_button.place(x=110, y=111)

l_info = Label(frame_settings, text='Category',height=1,anchor=NW,font=('Ivy 10 bold'),bg=co1,fg=co4)
l_info.place(x=10, y=160)

e_category = Entry(frame_settings, width=14, justify='left',relief='solid')
e_category.place(x=110, y=160)

img_add_category = Image.open('images/add.png')
img_add_category = img_add_category.resize((17, 17))
img_add_category = ImageTk.PhotoImage(img_add_category)
insert_expense_button = Button(frame_settings,command=insert_categories_b,image=img_add_category, text=" Add", width=80,compound=LEFT,
                 anchor=NW,font=("Ivy 7 bold"),bg=co1,fg=co0,overrelief=RIDGE)
insert_expense_button.place(x=110, y=190)


window.mainloop()