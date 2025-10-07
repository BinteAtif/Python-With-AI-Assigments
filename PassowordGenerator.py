import tkinter as tk
from tkinter import messagebox
import random
import string

# -----------------------------
# Advanced Password Generator
# -----------------------------

def generate_password():
    length = length_var.get()
    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digit_var.get()
    use_symbols = symbol_var.get()

    if not (use_upper or use_lower or use_digits or use_symbols):
        messagebox.showwarning("No Options", "Please select at least one character set!")
        return

    charset = ""
    if use_upper:
        charset += string.ascii_uppercase
    if use_lower:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation

    password = "".join(random.choice(charset) for _ in range(length))
    password_var.set(password)

    # Update history
    history_list.insert(0, password)
    if history_list.size() > 5:
        history_list.delete(5, tk.END)

    check_strength(password)


def copy_to_clipboard():
    pwd = password_var.get()
    if not pwd:
        messagebox.showinfo("Empty", "No password to copy!")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard!")


def check_strength(pwd):
    length = len(pwd)
    categories = sum([any(c.islower() for c in pwd),
                      any(c.isupper() for c in pwd),
                      any(c.isdigit() for c in pwd),
                      any(c in string.punctuation for c in pwd)])

    if length >= 12 and categories == 4:
        strength_var.set("Strength: Strong ✅")
        strength_label.config(fg="green")
    elif length >= 8 and categories >= 3:
        strength_var.set("Strength: Medium ⚠️")
        strength_label.config(fg="orange")
    else:
        strength_var.set("Strength: Weak ❌")
        strength_label.config(fg="red")


# --- UI ---
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x400")
root.resizable(False, False)

# Title
title = tk.Label(root, text="🔐 Advanced Password Generator", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Options Frame
options_frame = tk.Frame(root)
options_frame.pack(pady=10)

tk.Label(options_frame, text="Password Length:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
length_var = tk.IntVar(value=12)
length_entry = tk.Spinbox(options_frame, from_=4, to=50, textvariable=length_var, width=5, font=("Arial", 12))
length_entry.grid(row=0, column=1, padx=10)

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

tk.Checkbutton(options_frame, text="Include Uppercase", variable=upper_var, font=("Arial", 11)).grid(row=1, column=0, sticky="w")
tk.Checkbutton(options_frame, text="Include Lowercase", variable=lower_var, font=("Arial", 11)).grid(row=2, column=0, sticky="w")
tk.Checkbutton(options_frame, text="Include Numbers", variable=digit_var, font=("Arial", 11)).grid(row=1, column=1, sticky="w")
tk.Checkbutton(options_frame, text="Include Symbols", variable=symbol_var, font=("Arial", 11)).grid(row=2, column=1, sticky="w")

# Password Display
password_var = tk.StringVar(value="")
password_entry = tk.Entry(root, textvariable=password_var, font=("Arial", 16), justify="center", width=25)
password_entry.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

gen_btn = tk.Button(btn_frame, text="Generate", font=("Arial", 12), command=generate_password)
gen_btn.pack(side=tk.LEFT, padx=10)

copy_btn = tk.Button(btn_frame, text="Copy", font=("Arial", 12), command=copy_to_clipboard)
copy_btn.pack(side=tk.LEFT, padx=10)

# Strength Indicator
strength_var = tk.StringVar(value="Strength: —")
strength_label = tk.Label(root, textvariable=strength_var, font=("Arial", 12, "bold"))
strength_label.pack(pady=5)

# History
history_frame = tk.Frame(root)
history_frame.pack(pady=10)
tk.Label(history_frame, text="History (last 5):", font=("Arial", 12, "bold")).pack(anchor="w")

history_list = tk.Listbox(history_frame, height=5, width=40, font=("Arial", 11))
history_list.pack()

root.mainloop()
