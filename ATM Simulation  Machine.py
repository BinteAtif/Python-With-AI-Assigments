import tkinter as tk
from tkinter import messagebox, simpledialog

# Initial Setup
correct_name = "aasiyah syed"
correct_pin = "9753"
balance = 5000

# Global balance so it can be updated
user_balance = balance

# Function to handle login
def login():
    global name_entry, pin_entry
    name = name_entry.get().lower()
    pin = pin_entry.get()
    if name != correct_name:
        messagebox.showerror("Error", "Incorrect User Name")
        return
    if pin != correct_pin:
        messagebox.showerror("Error", "Incorrect PIN")
        return
    messagebox.showinfo("Success", f"Welcome {name}")
    show_menu()

# Function to display ATM menu
def show_menu():
    login_frame.pack_forget()
    menu_frame.pack()

# Balance check
def check_balance():
    messagebox.showinfo("Balance", f"Your balance is: Rs {user_balance}")

# Deposit money
def deposit_money():
    global user_balance
    amount = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
    if amount and amount > 0:
        user_balance += amount
        messagebox.showinfo("Deposit", f"Deposit successful. New balance: Rs {user_balance}")
    else:
        messagebox.showerror("Invalid", "Enter a valid amount.")

# Withdraw money
def withdraw_money():
    global user_balance
    amount = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
    if amount and 0 < amount <= user_balance:
        user_balance -= amount
        messagebox.showinfo("Withdraw", f"Withdrawal successful. New balance: Rs {user_balance}")
    else:
        messagebox.showerror("Invalid", "Insufficient balance or invalid amount.")

# Exit ATM
def exit_atm():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("ATM Machine")
root.geometry("300x300")

# --- Login Frame ---
login_frame = tk.Frame(root)

tk.Label(login_frame, text="Enter Name:").pack(pady=5)
name_entry = tk.Entry(login_frame)
name_entry.pack(pady=5)

tk.Label(login_frame, text="Enter PIN:").pack(pady=5)
pin_entry = tk.Entry(login_frame, show='*')
pin_entry.pack(pady=5)

tk.Button(login_frame, text="Login", command=login).pack(pady=10)

# --- Menu Frame ---
menu_frame = tk.Frame(root)

tk.Label(menu_frame, text="--- ATM Menu ---").pack(pady=10)
tk.Button(menu_frame, text="Check Balance", command=check_balance).pack(pady=5)
tk.Button(menu_frame, text="Deposit", command=deposit_money).pack(pady=5)
tk.Button(menu_frame, text="Withdraw", command=withdraw_money).pack(pady=5)
tk.Button(menu_frame, text="Exit", command=exit_atm).pack(pady=5)

# Start with login frame
login_frame.pack()

root.mainloop()
