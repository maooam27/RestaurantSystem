from tkinter import *

root = Tk()
root.title("Cassa")
root.geometry("800x600")


def SelectProduct(product):
    print(product)


# Operator name
op_zone = Frame(root, width=800, height=100)
op_zone.pack(pady=10, anchor=W)

op_label = Label(op_zone, text="Operator Code:")
op_label.pack(side=LEFT, anchor=W, padx=10)
operator_name = Entry(op_zone)
operator_name.pack(side=LEFT)

# Product list
product_zone = Frame(root, width=800, height=400)
product_zone.pack()

lambrusco = Button(product_zone, text="Lambrusco", width=10, height=5, command=lambda: SelectProduct("Lambrusco"))
lambrusco.grid(row=0, column=0, padx=15, pady=10)

rosso = Button(product_zone, text="Rosso", width=10, height=5)
rosso.grid(row=0, column=1, padx=15, pady=10)

bianco = Button(product_zone, text="Bianco", width=10, height=5)
bianco.grid(row=0, column=2, padx=15, pady=10)

bollicine = Button(product_zone, text="Bollicine", width=10, height=5)
bollicine.grid(row=0, column=3, padx=15, pady=10)

birra = Button(product_zone, text="Birra", width=10, height=5)
birra.grid(row=0, column=4, padx=15, pady=10)

if __name__ == "__main__":
    root.mainloop()
