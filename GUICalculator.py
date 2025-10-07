import tkinter as tk
from tkinter import ttk, messagebox
import math

# Scientific Calculator with Tabs + Dark Mode
root = tk.Tk()
root.title("Advanced Scientific Calculator")
root.geometry("420x580")
root.resizable(False, False)

# Entry Field
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=("Arial", 20), bd=8, relief="sunken", justify="right")
display.pack(fill="x", pady=10, padx=10)

# Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

basic_tab = tk.Frame(notebook)
scientific_tab = tk.Frame(notebook)

notebook.add(basic_tab, text="Basic")
notebook.add(scientific_tab, text="Scientific")

# Helper Functions

def insert(value):
    display_var.set(display_var.get() + str(value))

def clear():
    display_var.set("")

def backspace():
    current = display_var.get()
    display_var.set(current[:-1])

def calculate():
    try:
        expression = display_var.get().replace("^", "**")
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        display_var.set(str(result))
    except Exception:
        messagebox.showerror("Error", "Invalid Expression")
        display_var.set("")

# -----------------------------
# Button Builder
# -----------------------------
buttons = []  # keep track of all buttons for theme switching

def make_button(frame, text, row, col, cmd=None, colspan=1):
    if not cmd:
        cmd = lambda: insert(text)
    b = tk.Button(frame, text=text, width=6, height=2, font=("Arial", 14), command=cmd, bg="#f0f0f0", fg="black")
    b.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3, sticky="nsew")
    buttons.append(b)
    return b

# -----------------------------
# Basic Buttons
# -----------------------------

basic_layout = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

for r, row in enumerate(basic_layout):
    for c, char in enumerate(row):
        if char == "=":
            make_button(basic_tab, char, r, c, calculate)
        else:
            make_button(basic_tab, char, r, c)

make_button(basic_tab, "C", 4, 0, clear)
make_button(basic_tab, "⌫", 4, 1, backspace)
make_button(basic_tab, "(", 4, 2)
make_button(basic_tab, ")", 4, 3)

# -----------------------------
# Scientific Buttons
# -----------------------------

scientific_buttons = [
    ("sin", 0, 0, lambda: insert("math.sin(")),
    ("cos", 0, 1, lambda: insert("math.cos(")),
    ("tan", 0, 2, lambda: insert("math.tan(")),
    ("log", 0, 3, lambda: insert("math.log10(")),
    ("ln", 1, 0, lambda: insert("math.log(")),
    ("√", 1, 1, lambda: insert("math.sqrt(")),
    ("x²", 1, 2, lambda: insert("**2")),
    ("x³", 1, 3, lambda: insert("**3")),
    ("π", 2, 0, lambda: insert(str(math.pi))),
    ("e", 2, 1, lambda: insert(str(math.e))),
    ("exp", 2, 2, lambda: insert("math.exp(")),
    ("^", 2, 3, lambda: insert("^")),
    ("fact", 3, 0, lambda: insert("math.factorial(")),
    ("1/x", 3, 1, lambda: insert("1/")),
    ("%", 3, 2, lambda: insert("/100")),
    ("=", 3, 3, calculate),
]

for text, r, c, cmd in scientific_buttons:
    make_button(scientific_tab, text, r, c, cmd)

# -----------------------------
# Keyboard Bindings
# -----------------------------

def key_handler(event):
    if event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        backspace()
    elif event.char in "0123456789+-*/().^":
        insert(event.char)

root.bind("<Key>", key_handler)

# -----------------------------
# Dark Mode Toggle
# -----------------------------

dark_mode = False

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.config(bg="#2e2e2e")
        display.config(bg="#3c3c3c", fg="white", insertbackground="white")
        for b in buttons:
            b.config(bg="#4a4a4a", fg="white")
        theme_btn.config(text="☀ Light Mode", bg="#444", fg="white")
    else:
        root.config(bg="SystemButtonFace")
        display.config(bg="white", fg="black", insertbackground="black")
        for b in buttons:
            b.config(bg="#f0f0f0", fg="black")
        theme_btn.config(text="🌙 Dark Mode", bg="#ddd", fg="black")

# Theme toggle button
theme_btn = tk.Button(root, text="🌙 Dark Mode", font=("Arial", 12), command=toggle_theme)
theme_btn.pack(pady=8)

root.mainloop()
