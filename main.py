import tkinter as tk
from tkinter import messagebox

def run():
    initial = initial_state.get().strip()
    states = [s.strip() for s in all_states.get().split(',')]
    alphabet_set = [a.strip() for a in alphabet.get().split(',')]
    accepting = set(a.strip() for a in accepting_states.get().split(','))

    transition_set = {}
    for rule in transitions.get().split(';'):
        try:
            from_state, symbol, to_state = [part.strip() for part in rule.strip().split('-')]
            transition_set[(from_state, symbol)] = to_state
        except ValueError:
            result_label.config(text=f"Invalid transition format: '{rule}'")
            return

    dfa = {
        "states": states,
        "alphabet": alphabet_set,
        "initial_state": initial,
        "accepting_states": accepting,
        "transitions": transition_set
    }

    print("DFA Structure:")
    for k, v in dfa.items():
        print(f"{k}: {v}")


# Main 
root = tk.Tk()
root.title("DFA")
root.config(padx=30, pady=30) 
root.geometry("1000x400")

initial_state = tk.StringVar()
all_states = tk.StringVar()
alphabet = tk.StringVar()
transitions = tk.StringVar()
accepting_states = tk.StringVar()
input_string = tk.StringVar()


tk.Label(root, text="Enter Initial State: ").grid(row=1, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=initial_state, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Enter All States: ").grid(row=2, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=all_states, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Alphabet: ").grid(row=3, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=alphabet, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Transitions: ").grid(row=4, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=transitions, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Accepting State(s): ").grid(row=5, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=accepting_states, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Input String to Test: ").grid(row=6, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=input_string, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=6, column=1, padx=5, pady=5)

tk.Button(root, text="Run", command=run).grid(row=7, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.grid(row=9, column=0, columnspan=2, pady=10)


root.mainloop()