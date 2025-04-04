import tkinter as tk
from tkinter import messagebox


#initial_state = input("Enter initial state: ")
#states = input("Enter all states: ").split(', ')
#alphabet = input("Enter alphabet: ").split(', ')
#accepting_states = input("Enter accepting state(s): ").split(', ')

def run():
    initial = initial_state.get().strip()
    states = all_states.get().split(',')
    alphabet_set = alphabet.get().split(',')
    accepting = accepting_states.get().split(',')

    print("Initial State:", initial)
    print("All States:", states)
    print("Alphabet:", alphabet_set)
    print("Accepting States:", accepting)

# Main 
root = tk.Tk()
root.title("DFA")
root.config(padx=30, pady=30) 
root.geometry("600x300")

initial_state = tk.StringVar()
all_states = tk.StringVar()
alphabet = tk.StringVar()
accepting_states = tk.StringVar()

tk.Label(root, text="Enter Initial State: ").grid(row=1, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=initial_state).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Enter All States: ").grid(row=2, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=all_states).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Alphabet: ").grid(row=3, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=alphabet).grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Accepting State(s): ").grid(row=4, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=accepting_states).grid(row=4, column=1, padx=5, pady=5)

tk.Button(root, text="Run", command=run).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()