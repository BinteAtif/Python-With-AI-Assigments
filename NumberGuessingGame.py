import tkinter as tk
import random

# -----------------------------
# Advanced Number Guessing Game
# -----------------------------

RANGES = {"Easy": 50, "Medium": 80, "Hard" : 110}

# --- Game State ---
difficulty = "Medium"
secret_number = None
attempts = 0
min_possible = 1
max_possible = RANGES[difficulty]
previous_guesses = []

# --- Logic ---
def start_new_game():
    global secret_number, attempts, min_possible, max_possible, previous_guesses
    attempts = 0
    previous_guesses = []
    min_possible = 1
    max_possible = RANGES[difficulty]
    secret_number = random.randint(1, RANGES[difficulty])

    status_var.set("Guess the number!")
    attempts_var.set("Attempts: 0")
    range_var.set(f"Range: {min_possible}–{max_possible}")
    guesses_var.set("Guesses: —")
    guess_entry.config(state=tk.NORMAL)
    guess_btn.config(state=tk.NORMAL)
    guess_entry.delete(0, tk.END)
    guess_entry.focus_set()

def set_difficulty(new_diff):
    global difficulty
    difficulty = new_diff
    range_info_label.config(text=f"Target is between 1 and {RANGES[difficulty]}")
    start_new_game()

def check_guess(event=None):
    global attempts, min_possible, max_possible
    raw = guess_entry.get().strip()
    if not raw:
        status_var.set("Enter a number first.")
        return
    try:
        g = int(raw)
    except ValueError:
        status_var.set("Please enter a valid integer.")
        return

    if not (1 <= g <= RANGES[difficulty]):
        status_var.set(f"Out of range! Use 1–{RANGES[difficulty]}.")
        return

    attempts += 1
    attempts_var.set(f"Attempts: {attempts}")

    previous_guesses.append(g)
    guesses_var.set("Guesses: " + ", ".join(map(str, previous_guesses)))

    if g < secret_number:
        if g + 1 > min_possible:
            min_possible = g + 1
        range_var.set(f"Range: {min_possible}–{max_possible}")
        hint = "Too low"
        if abs(secret_number - g) <= max(3, RANGES[difficulty] // 20):
            hint += "… but very close!"
        status_var.set(hint)
    elif g > secret_number:
        if g - 1 < max_possible:
            max_possible = g - 1
        range_var.set(f"Range: {min_possible}–{max_possible}")
        hint = "Too high"
        if abs(secret_number - g) <= max(3, RANGES[difficulty] // 20):
            hint += "… but very close!"
        status_var.set(hint)
    else:
        status_var.set(f"🎉 Correct! The number was {secret_number}.")
        guess_btn.config(state=tk.DISABLED)
        guess_entry.config(state=tk.DISABLED)

def give_up():
    status_var.set(f"😅 You gave up! It was {secret_number}.")
    guess_btn.config(state=tk.DISABLED)
    guess_entry.config(state=tk.DISABLED)

# --- UI ---
root = tk.Tk()
root.title("Advanced Number Guessing Game")
root.geometry("520x420")
root.resizable(False, False)

title = tk.Label(root, text="🔢 Number Guessing Game", font=("Arial", 18, "bold"))
title.pack(pady=(12, 4))

controls = tk.Frame(root)
controls.pack(pady=4)

tk.Label(controls, text="Difficulty:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=(0, 6))
for diff in ("Easy", "Medium", "Hard"):
    tk.Button(controls, text=diff, font=("Arial", 11), command=lambda d=diff: set_difficulty(d)).pack(side=tk.LEFT, padx=4)

range_info_label = tk.Label(root, text=f"Target is between 1 and {RANGES[difficulty]}", font=("Arial", 11))
range_info_label.pack(pady=(0, 8))

input_row = tk.Frame(root)
input_row.pack(pady=6)

guess_entry = tk.Entry(input_row, font=("Arial", 16), width=10, justify="center")
guess_entry.pack(side=tk.LEFT, padx=6)

guess_btn = tk.Button(input_row, text="Guess", font=("Arial", 14), command=check_guess)
guess_btn.pack(side=tk.LEFT, padx=6)

new_btn = tk.Button(input_row, text="New Game", font=("Arial", 12), command=start_new_game)
new_btn.pack(side=tk.LEFT, padx=6)

giveup_btn = tk.Button(input_row, text="Give Up", font=("Arial", 12), command=give_up)
giveup_btn.pack(side=tk.LEFT, padx=6)

status_var = tk.StringVar(value="Guess the number!")
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 13))
status_label.pack(pady=(8, 2))

attempts_var = tk.StringVar(value="Attempts: 0")
attempts_label = tk.Label(root, textvariable=attempts_var, font=("Arial", 11))
attempts_label.pack()

range_var = tk.StringVar(value=f"Range: {min_possible}–{max_possible}")
range_label = tk.Label(root, textvariable=range_var, font=("Arial", 11))
range_label.pack()

guesses_var = tk.StringVar(value="Guesses: —")
prev_label = tk.Label(root, textvariable=guesses_var, font=("Arial", 11), wraplength=480, justify="left")
prev_label.pack(padx=10, pady=(10, 0))

root.bind("<Return>", check_guess)

start_new_game()
root.mainloop()
