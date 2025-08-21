import time
import tkinter as tk
import json
from tkinter import font
from tkinter import messagebox


basket = []
root = tk.Tk()
root.geometry("1500x900")
root.title("Main Checkout Screen")

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

with open("productDatabase.json", "r") as f:
    product_data = json.load(f)

for product in product_data:
    print(product['name'])
    global correction_mode_status
    global stocking_mode_status
    def addProduct(p=product):
        if not stocking_mode_status and not correction_mode_status:
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
        if not stocking_mode_status:
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
        else:
            # User is trying to stock products
            print("stocking")
            for product in product_data:
                if product['name'] == p['name']:
                    print(product['stock'])
                    product['stock'] += 1
                    print(product['stock'])
                    for itemButton in product_list.winfo_children():
                        if p['name'] in itemButton['text']:
                            print("correct")
                            print(product['stock'])
                            itemButton.config(text=f"{product['name']} | £{product['price']} ({product['stock']})")

        print(basket)
        render_basket()
    product_button = tk.Button(product_list, text=f"{product['name']} | £{product['price']} ({product['stock']})", bg="green", font=font.Font(size=15), command=addProduct)
    product_button.pack(pady="1", fill="x")

# Draw transaction progress

products_added = tk.Frame(root, width="750", height="450")  # This'll be used to add current items and show subtotal
products_added.grid(column=0, row=0, sticky="nsew", padx=0, pady=0)
products_added.grid_propagate(False)

subtotal = tk.Label(products_added, text="Subtotal: £0.00", font=font.Font(weight="bold"), anchor="w")
subtotal.pack(side="bottom", fill="x")


# Draw action buttons

action_container = tk.Frame(root, width="750", height="900")
action_container.grid(column=1, row=0, rowspan=2, sticky="nsew", padx=0, pady=0)
action_container.grid_propagate(False)

def checkout():
    if len(basket) > 0:
        checkout = tk.Toplevel(root)
        checkout.geometry("1500x900")
        checkout.title("Transaction Payment")
        checkout.grab_set()
        checkout.focus_set()
        checkout.transient(root)

        checkout.grid_columnconfigure(0, minsize=750)
        checkout.grid_columnconfigure(1, minsize=750)

        product_listCheckout = tk.Frame(checkout, width="750", height="900")
        product_listCheckout.grid(column=0, sticky="nsew", padx=0, pady=0)
        product_listCheckout.grid_propagate(False)

        for product in basket:
            border = tk.Frame(product_listCheckout, bd=2, bg="black")
            border.pack(fill="x")
            label = tk.Label(border, text=f"{product['name']} | {product['quantity']}", font=font.Font(size=13), anchor="w")
            label.pack(fill="x", padx=1, pady=1)

        border = tk.Frame(product_listCheckout, bd=2, bg="black")
        border.pack(fill="x")
        outstanding_balance = sum([basketItem['price'] * basketItem['quantity'] for basketItem in basket])
        totalLabel = tk.Label(border, text=f"Total: £{outstanding_balance:.2f}", anchor="w", font=font.Font(weight="bold", size=17), bg="white")
        totalLabel.pack(side="bottom", fill="x")

        outstanding_label = tk.Label(checkout, text=f"DUE: £{outstanding_balance:.2f}", font=font.Font(size=30))
        outstanding_label.grid(column=1, row=0, sticky="nsew", padx=0, pady=0)

        def deductCash(amount):
            nonlocal outstanding_balance
            outstanding_balance -= amount
            if outstanding_balance > 0:
                outstanding_label.config(text=f"DUE: £{outstanding_balance:.2f}")
            elif outstanding_balance < 0:
                outstanding_label.config(text=f"CHANGE: £{abs(outstanding_balance):.2f}")
                messagebox.showinfo("Transaction complete", "The transaction is now complete, you may close this window!")

        quickCashFrame = tk.Frame(checkout)
        quickCashFrame.grid(column=1, padx=0, pady=0)

        quickOnePound = tk.Button(quickCashFrame, text="£1", bg="beige", font=font.Font(size=20), command=lambda: deductCash(1))
        quickOnePound.grid(column=1, row=1, padx=0, pady=0)
        quickFivePound = tk.Button(quickCashFrame, text="£5", bg="beige", font=font.Font(size=20), command=lambda: deductCash(5))
        quickFivePound.grid(column=2, row=1, padx=0, pady=0)
        quickTenPound = tk.Button(quickCashFrame, text="£10", bg="beige", font=font.Font(size=20), command=lambda: deductCash(10))
        quickTenPound.grid(column=3, row=1,padx=0, pady=0)
        quickTwentyPound = tk.Button(quickCashFrame, text="£20", bg="beige", font=font.Font(size=20), command=lambda: deductCash(20))
        quickTwentyPound.grid(column=4, row=1, padx=0, pady=0)

        enterValueContainer = tk.Frame(checkout)
        enterValueContainer.grid(column=1, padx=5)
        enterValueContainer.columnconfigure(0, weight=3)
        enterValueContainer.columnconfigure(1, weight=2)
        exactValue = tk.Entry(enterValueContainer, font=font.Font(size=17))
        exactValue.grid(column=0, row=0, sticky="nsew")

        def deductExact():
            try:
                toDeduct = float(exactValue.get())
                deductCash(toDeduct)
            except ValueError:
                messagebox.showerror("Incorrect value", "Please enter a decimal value into the input box.")

        enterExactValue = tk.Button(enterValueContainer, bg="green", text="Deduct", font=font.Font(size=17), command=deductExact)
        enterExactValue.grid(column=1, row=0, sticky="nsew")

        def paymentFinish():
            outstanding_label.config(text=f"Card payment successful!")
            messagebox.showinfo("Transaction complete", "The transaction is now complete, you may close this window!")

        def payCard():
            outstanding_label.config(text=f"Awaiting card payment of £{outstanding_balance:.2f}...")
            checkout.after(3000, paymentFinish)

        tk.Button(checkout, bg="lightgreen", text="Card", font=font.Font(size=17), command=payCard).grid(column=1, row=3, sticky="nsew", pady="5")
    else:
        messagebox.showerror("Invalid action", "Cannot complete a transaction with an empty basket.")

finish_and_pay = tk.Button(action_container, bg="lightgreen", font=font.Font(size=20), text="Collect payment", command=checkout)
finish_and_pay.pack(fill="x", padx="5", pady=(0,5))

correction_mode_status = False
stocking_mode_status = False
def toggle_correction_mode():
    global correction_mode_status
    if correction_mode_status:
        correction_mode_status = False
        correction_mode.config(text="Correction mode")
        action_container.config(bg="white")
    elif not stocking_mode_status:
        correction_mode_status = True
        correction_mode.config(text="Leave correction mode")
        action_container.config(bg="pink")
    else:
        messagebox.showwarning("Invalid action.", "Please disable stocking mode to use correction mode.")

def toggle_stocking_mode():
    global stocking_mode_status
    if stocking_mode_status:
        stocking_mode_status = False
        stocking_mode.config(text="Correction mode")
        action_container.config(bg="white")
    else:
        basket.clear()
        stocking_mode_status = True
        stocking_mode.config(text="Leave stocking mode")
        action_container.config(bg="lightblue")

correction_mode = tk.Button(action_container, bg="darkred", font=font.Font(size=17), text="Correction mode", command=toggle_correction_mode)
correction_mode.pack(fill="x", padx="5")

stocking_mode = tk.Button(action_container, bg="lightblue", font=font.Font(size=17), text="Stocking mode", command=toggle_stocking_mode)
stocking_mode.pack(fill="x", padx="5")

def logout():
    with open("productDatabase.json", "w") as f:
        json.dump(product_data, f, indent=4)
    root.destroy()

logout = tk.Button(action_container, bg="lightgray", font=font.Font(size=23), text="Logout", command=logout)
logout.pack(fill="x", padx="5", side="bottom")

root.mainloop()
