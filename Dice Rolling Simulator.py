import tkinter as tk
import random

# Unicode dice characters for 1–6
dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

# Function to roll the dice
def roll_dice():
    dice_number = random.randint(1, 6)
    dice_label.config(text=dice_faces[dice_number - 1], font=("Arial", 120))
    number_label.config(text=f"You rolled: {dice_number}", font=("Arial", 16))

# Create the main window
root = tk.Tk()
root.title("Dice Rolling Game")
root.geometry("300x400")
root.resizable(False, False)

# Title label
title_label = tk.Label(root, text="🎲 Dice Roller 🎲", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Dice face label
dice_label = tk.Label(root, text="⚀", font=("Arial", 120))
dice_label.pack(pady=20)

# Number result label
number_label = tk.Label(root, text="Roll the dice!", font=("Arial", 16))
number_label.pack(pady=10)

# Button to roll dice
roll_button = tk.Button(root, text="Roll Dice", font=("Arial", 16), command=roll_dice)
roll_button.pack(pady=20)

# Run the GUI loop
root.mainloop()

