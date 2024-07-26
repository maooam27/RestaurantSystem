import time
from tkinter import *
import sqlite3
import tkinter.messagebox as messagebox
import socket

bar_port = 25728
pizzeria_port = 25729
kitchen_port = 25730

current_order = ""
actual_order = []
current_price: float = 0.0

menu = {
    "bar": ["Lambrusco", "Rosso", "Bianco", "Bollicine", "Birra", "Fanta"],
    "pizzeria": ["Margherita", "Marinara", "Diavola", "Viennese", "Capricciosa", "Quattro Stagioni"],
    "cucina": ["Spaghetti", "Penne", "Risotto", "Tagliatelle", "Lasagne", "Ravioli"]
}

bar_orders = []
pizzeria_orders = []
kitchen_orders = []

root = Tk()
root.title("Cassa")
root.geometry("800x600")

# Clear the database and autoincrement
db = sqlite3.connect("CurrentDay.db")
cursor = db.cursor()
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
db.commit()
db.close()


def pay_table():
    if table_paying.get() == "" or " " in table_paying.get():
        return messagebox.showinfo("Error", "Insert the table number")
    db = sqlite3.connect("CurrentDay.db")
    curs = db.cursor()
    curs.execute(f"SELECT * FROM orders WHERE table_number = {table_paying.get()}")
    orders = curs.fetchall()
    db.commit()
    db.close()

    if not orders:
        return messagebox.showinfo("Error", "Table not found")

    total_price = 0.0
    for order in orders:
        total_price += order[6]

    db = sqlite3.connect("CurrentDay.db")
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM orders WHERE table_number = {table_paying.get()}")
    db.commit()
    db.close()

    return messagebox.showinfo("Payment", f"Table {table_paying.get()} paid {total_price}€")


def update_time():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=str(current_time))
    root.after(1000, update_time)


def SelectProduct(product, price):
    global current_order, current_price
    current_order += product + ", "
    current_price += price
    return


def division():
    global actual_order, current_order, bar_orders
    actual_order = current_order.split(", ")
    for i in range(len(actual_order)):
        if actual_order[i] == "":
            actual_order.pop(i)
            continue
        if actual_order[i] in menu["bar"]:
            bar_orders.append(actual_order[i])
        elif actual_order[i] in menu["pizzeria"]:
            pizzeria_orders.append(actual_order[i])
        elif actual_order[i] in menu["cucina"]:
            kitchen_orders.append(actual_order[i])

    return


# noinspection DuplicatedCode
def SendOrder():
    global current_order, current_price, actual_order, bar_orders, pizzeria_orders, kitchen_orders
    if (operator_name.get() == "" or n_table.get() == "") or (" " in operator_name.get() or " " in n_table.get()):
        print("Fill operator code and table number")
        return messagebox.showinfo("Error", "Fill operator code and table number")
    elif current_order == "":
        print("Select a product")
        return messagebox.showinfo("Error", "Select a product")

    division()

    # Server management

    # Bar
    if bar_orders:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', bar_port))
        s.sendall(f"From table: {n_table.get()}\n".encode())
        for i in range(len(bar_orders)):
            s.sendall(f"\t{bar_orders[i]}\n".encode())
        s.close()
    # Pizzeria
    if pizzeria_orders:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', pizzeria_port))
        s.sendall(f"From table: {n_table.get()}\n".encode())
        for i in range(len(pizzeria_orders)):
            s.sendall(f"\t{pizzeria_orders[i]}\n".encode())
        s.close()
    # Kitchen
    if kitchen_orders:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', kitchen_port))
        s.sendall(f"From table: {n_table.get()}\n".encode())
        for i in range(len(kitchen_orders)):
            s.sendall(f"\t{kitchen_orders[i]}\n".encode())
        s.close()

    # Database management
    database = sqlite3.connect("CurrentDay.db")
    c = database.cursor()
    c.execute(f"INSERT INTO orders VALUES (NULL, '{n_table.get()}', '{str(time.strftime('%H:%M:%S'))}',"
              f" '{operator_name.get()}', '{current_order}', {current_price})")
    print(n_table.get(), time.strftime('%H:%M:%S'), operator_name.get(), current_order)
    database.commit()
    database.close()

    current_order = ""
    current_price = 0.0
    actual_order = []
    bar_orders = []
    pizzeria_orders = []
    kitchen_orders = []
    return


# Operator name
op_zone = Frame(root, width=800, height=100)
op_zone.pack(pady=10, anchor=W, fill=X)

op_label = Label(op_zone, text="Operator Code:")
op_label.pack(side=LEFT, anchor=W, padx=10)
operator_name = Entry(op_zone)
operator_name.pack(side=LEFT)

clock_label = Label(op_zone, text="00:00:00")
clock_label.pack(side=RIGHT, anchor=E, padx=10)

n_table = Entry(op_zone, width=3)
n_table.pack(side=RIGHT, padx=10)

table_label = Label(op_zone, text="Table:")
table_label.pack(side=RIGHT, padx=10)

send_order = Button(op_zone, text="Send Order", command=SendOrder)
send_order.pack(side=RIGHT, padx=10)

# Product list

# Bar
product_zone = Frame(root, width=800, height=400)
product_zone.pack()

lambrusco = Button(product_zone, text="Lambrusco", width=10, height=5, command=lambda: SelectProduct("Lambrusco", 6.0))
lambrusco.grid(row=0, column=0, padx=3, pady=10)

rosso = Button(product_zone, text="Rosso", width=10, height=5, command=lambda: SelectProduct("Rosso", 5.0))
rosso.grid(row=0, column=1, padx=3, pady=10)

bianco = Button(product_zone, text="Bianco", width=10, height=5, command=lambda: SelectProduct("Bianco", 4.0))
bianco.grid(row=0, column=2, padx=3, pady=10)

bollicine = Button(product_zone, text="Bollicine", width=10, height=5, command=lambda: SelectProduct("Bollicine", 7.0))
bollicine.grid(row=0, column=3, padx=3, pady=10)

birra = Button(product_zone, text="Birra", width=10, height=5, command=lambda: SelectProduct("Birra", 3.0))
birra.grid(row=0, column=4, padx=3, pady=10)

fanta = Button(product_zone, text="Fanta", width=10, height=5, command=lambda: SelectProduct("Fanta", 3.5))
fanta.grid(row=0, column=5, padx=3, pady=10)


product_zone2 = Frame(root, width=800, height=400)
product_zone2.pack()

margherita = Button(product_zone, text="Margherita", width=10, height=5,
                    command=lambda: SelectProduct("Margherita", 4.5))
margherita.grid(row=1, column=0, padx=3, pady=10)

marinara = Button(product_zone, text="Marinara", width=10, height=5,
                  command=lambda: SelectProduct("Marinara", 5.0))
marinara.grid(row=1, column=1, padx=3, pady=10)

diavola = Button(product_zone, text="Diavola", width=10, height=5,
                 command=lambda: SelectProduct("Diavola", 5.5))
diavola.grid(row=1, column=2, padx=3, pady=10)

viennese = Button(product_zone, text="Viennese", width=10, height=5,
                  command=lambda: SelectProduct("Viennese", 5.5))
viennese.grid(row=1, column=3, padx=3, pady=10)

capricciosa = Button(product_zone, text="Capricciosa", width=10, height=5,
                     command=lambda: SelectProduct("Capricciosa", 5.0))
capricciosa.grid(row=1, column=4, padx=3, pady=10)

quattro_stagioni = Button(product_zone, text="Quattro Stagioni", width=10, height=5,
                          command=lambda: SelectProduct("Quattro Stagioni", 5.5))
quattro_stagioni.grid(row=1, column=5, padx=3, pady=10)


product_zone3 = Frame(root, width=800, height=400)
product_zone3.pack()

spaghetti = Button(product_zone, text="Spaghetti", width=10, height=5, command=lambda: SelectProduct("Spaghetti", 10.0))
spaghetti.grid(row=2, column=0, padx=3, pady=10)

penne = Button(product_zone, text="Penne", width=10, height=5, command=lambda: SelectProduct("Penne", 10.0))
penne.grid(row=2, column=1, padx=3, pady=10)

risotto = Button(product_zone, text="Risotto", width=10, height=5, command=lambda: SelectProduct("Risotto", 9.0))
risotto.grid(row=2, column=2, padx=3, pady=10)

tagliatelle = Button(product_zone, text="Tagliatelle", width=10, height=5,
                     command=lambda: SelectProduct("Tagliatelle", 10.0))
tagliatelle.grid(row=2, column=3, padx=3, pady=10)

lasagne = Button(product_zone, text="Lasagne", width=10, height=5, command=lambda: SelectProduct("Lasagne", 12.0))
lasagne.grid(row=2, column=4, padx=3, pady=10)

ravioli = Button(product_zone, text="Ravioli", width=10, height=5, command=lambda: SelectProduct("Ravioli", 10.5))
ravioli.grid(row=2, column=5, padx=3, pady=10)


pay_zone = Frame(root, width=800, height=100)
pay_zone.pack(pady=10, anchor=W, fill=X)

pay_button = Button(pay_zone, text="Paga", command=pay_table)
pay_button.pack(side=RIGHT, padx=10)

table_paying = Entry(pay_zone, width=3)
table_paying.pack(side=RIGHT, padx=10)

# TODO: search for data in the database of the day
# https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

if __name__ == "__main__":
    update_time()
    root.mainloop()
