import time
from tkinter import *
import sqlite3
import tkinter.messagebox as messagebox
import socket

root = Tk()
root.title("Cassa")
root.geometry("800x600")

current_order = ""


# Clear the database and autoincrement
db = sqlite3.connect("CurrentDay.db")
cursor = db.cursor()
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
db.commit()
db.close()


def update_time():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=str(current_time))
    root.after(1000, update_time)


def SelectProduct(product):
    global current_order
    current_order += product + ", "


def SendOrder():
    global current_order
    if (operator_name.get() == "" or n_table.get() == "") or (" " in operator_name.get() or " " in n_table.get()):
        print("Fill operator code and table number")
        return messagebox.showinfo("Error", "Fill operator code and table number")
    elif current_order == "":
        print("Select a product")
        return messagebox.showinfo("Error", "Select a product")
    database = sqlite3.connect("CurrentDay.db")
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO orders VALUES (NULL, '{n_table.get()}', '{str(time.strftime('%H:%M:%S'))}',"
                   f" '{operator_name.get()}', '{current_order}')")
    print(n_table.get(), time.strftime('%H:%M:%S'), operator_name.get(), current_order)
    database.commit()
    database.close()
    current_order = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 4384))
    s.sendall(b"Order sent")
    s.close()
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
product_zone = Frame(root, width=800, height=400)
product_zone.pack()

lambrusco = Button(product_zone, text="Lambrusco", width=10, height=5, command=lambda: SelectProduct("Lambrusco"))
lambrusco.grid(row=0, column=0, padx=3, pady=10)

rosso = Button(product_zone, text="Rosso", width=10, height=5, command=lambda: SelectProduct("Rosso"))
rosso.grid(row=0, column=1, padx=3, pady=10)

bianco = Button(product_zone, text="Bianco", width=10, height=5, command=lambda: SelectProduct("Bianco"))
bianco.grid(row=0, column=2, padx=3, pady=10)

bollicine = Button(product_zone, text="Bollicine", width=10, height=5, command=lambda: SelectProduct("Bollicine"))
bollicine.grid(row=0, column=3, padx=3, pady=10)

birra = Button(product_zone, text="Birra", width=10, height=5, command=lambda: SelectProduct("Birra"))
birra.grid(row=0, column=4, padx=3, pady=10)

fanta = Button(product_zone, text="Fanta", width=10, height=5, command=lambda: SelectProduct("Fanta"))
fanta.grid(row=0, column=5, padx=3, pady=10)

if __name__ == "__main__":
    update_time()
    root.mainloop()
