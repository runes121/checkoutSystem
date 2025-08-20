import tkinter as tk
import json
from tkinter import font
from tkinter import messagebox


basket = []
root = tk.Tk()
root.geometry("1500x900")

root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=2)
root.grid_rowconfigure(0, weight=3)
root.grid_rowconfigure(1, weight=2)
# Draw product list UI

product_list = tk.Frame(root, width="750", height="450")
product_list.grid(column=0, row=1, sticky="nsew", padx=0, pady=0)
product_list.grid_propagate(False)

def render_basket():
    print("rendering basket")
    for text in products_added.winfo_children():
        if "subtotal" not in text["text"].lower():
            text.destroy()
    for item in basket:
        label = tk.Label(products_added, text=f"{item['name']} | {item['quantity']}")
        label.pack()
    print("rendering subtotal")
    subtotal.config(text=f"Subtotal: £{sum([basketItem['price'] * basketItem['quantity'] for basketItem in basket]):.2f}")


product_data = json.load(open("productDatabase.json", "r"))
for product in product_data:
    print(product['name'])
    def addProduct(p=product):
        for product in product_data:
            if product['name'] == p['name']:
                if product['stock'] > 0:
                    product['stock'] -= 1
                    for itemButton in product_list.winfo_children():
                        if p['name'] in itemButton['text']:
                            itemButton.config(text=f"{product['name']} | £{product['price']} ({product['stock']})")
                else:
                    print("Product out of stock!")
                    messagebox.showwarning("Out of stock!", f"{product['name']} is out of stock. Please update stock if this is false.")
        global correction_mode_status
        if p in basket:
            for item in basket:
                if item == p:
                    if correction_mode_status:
                        if item['quantity'] == 1:
                            basket.remove(p)
                        else:
                            item['quantity'] -= 1
                    else:
                        item['quantity'] += 1
        else:
            if not correction_mode_status:
                p['quantity'] = 1
                basket.append(p)
        print(basket)
        render_basket()
    product_button = tk.Button(product_list, text=f"{product['name']} | £{product['price']} ({product['stock']})", bg="green", font=font.Font(size=15), command=addProduct)
    product_button.pack(pady="1", fill="x")

# Draw transaction progress

products_added = tk.Frame(root, width="750", height="450")  # This'll be used to add current items and show subtotal
products_added.grid(column=0, row=0, sticky="nsew", padx=0, pady=0)
products_added.grid_propagate(False)

subtotal = tk.Label(products_added, text="Current subtotal: £0.00", font=font.Font(weight="bold"), anchor="w")
subtotal.pack(side="bottom", fill="x")


# Draw action buttons

action_container = tk.Frame(root, width="750", height="900")
action_container.grid(column=1, row=0, rowspan=2, sticky="nsew", padx=0, pady=0)
action_container.grid_propagate(False)

finish_and_pay = tk.Button(action_container, bg="lightgreen", font=font.Font(size=20), text="Collect payment")
finish_and_pay.pack(fill="x", padx="5", pady=(0,5))

correction_mode_status = False
def toggle_correction_mode():
    global correction_mode_status
    if correction_mode_status:
        correction_mode_status = False
        correction_mode.config(text="Correction mode")
        action_container.config(bg="white")
    else:
        correction_mode_status = True
        correction_mode.config(text="Leave correction mode")
        action_container.config(bg="pink")

correction_mode = tk.Button(action_container, bg="darkred", font=font.Font(size=17), text="Correction mode", command=toggle_correction_mode)
correction_mode.pack(fill="x", padx="5")

stocking_mode = tk.Button(action_container, bg="lightblue", font=font.Font(size=17), text="Stocking mode")
stocking_mode.pack(fill="x", padx="5")

logout = tk.Button(action_container, bg="lightgray", font=font.Font(size=23), text="Logout")
logout.pack(fill="x", padx="5", side="bottom")

root.mainloop()
