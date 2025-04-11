import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import graphviz

#Visualize String button
def run_string():
    initial = initial_state.get().strip()
    states = [s.strip() for s in all_states.get().split(',')]
    alphabet_set = [a.strip() for a in alphabet.get().split(',')]
    accepting = set(a.strip() for a in accepting_states.get().split(','))

    transition_set = {}
    input_str = input_string.get().strip()
    
    if not input_str:
        result_label.config(text="No input string provided", fg="orange")
        return
    
    for rule in transitions.get().split(';'):
        try:
            from_state, symbol, to_state = [part.strip() for part in rule.strip().split('-')]
            transition_set[(from_state, symbol)] = to_state
        except ValueError:
            result_label.config(text=f"Invalid transition format: '{rule}'", fg="red")
            return
    
    steps = []
    current_state = initial
    for symbol in input_str:
        if symbol not in alphabet_set:
            result_label.config(text=f"Symbol '{symbol}' not in alphabet.", fg="red")
            return
        if (current_state, symbol) not in transition_set:
            result_label.config(text=f"No transition from {current_state} with symbol '{symbol}'", fg="red")
            return
        next_state = transition_set[(current_state, symbol)]
        steps.append((current_state, symbol, next_state))
        current_state = next_state
    
    # Display window for transition state
    displayer = tk.Toplevel()
    displayer.title("DFA Transitions")
    displayer.geometry("+800+100")
    # output.resizable(False, False)

    # Initial DFA creation
    dfa_graph = graphviz.Digraph()

    for state in states:
        if state in accepting:
            dfa_graph.attr('node', shape='doublecircle')
        else:
            dfa_graph.attr('node', shape='circle')
        dfa_graph.node(state)

    dfa_graph.attr('node', shape='plaintext')
    dfa_graph.node('start', label='')
    dfa_graph.edge('start', initial)

    for (from_state, symbol), to_state in transition_set.items():
        dfa_graph.edge(from_state, to_state, label=symbol)

    dfa_graph.render('dfa', format='png', view=False)

    dfa_image = Image.open("dfa.png")
    dfa_photo = ImageTk.PhotoImage(dfa_image)
    dfa_label = tk.Label(displayer, image=dfa_photo)
    dfa_label.pack()

    step_index = tk.IntVar(value=-1)
    dynamic_string = tk.StringVar(value="")

    # Changes the DFA displayed on command
    def current_transition():

        current = step_index.get()
        total = len(steps)
      
        #Updates labels
        if current >= total:
            transition_label.config(text="No more steps.")
            return
        
        from_state, symbol, to_state = steps[current]
        current_text = f"Transition {current + 1} of {total}: {from_state} --{symbol}--> {to_state}"

        string_label.config(text=f"String: '{dynamic_string.get()}'")
        transition_label.config(text=current_text)

        if current < total-1:
            current_label.config(text=f"Current State: {from_state}")
            next_label.config(text=f"Next State: {to_state}")
        else:
            current_label.config(text=f"Final State: {to_state}")
        
        if current == total -1:
            if to_state in accepting:
                next_label.config(text="Accepted!", fg="green")
            else:
                next_label.config(text="Rejected.", fg="red")

        # Creates DFA
        dfa_graph = graphviz.Digraph()

        for state in states:
            if state in accepting:
                dfa_graph.attr('node', shape='doublecircle')
            else:
                dfa_graph.attr('node', shape='circle')
            dfa_graph.node(state)

            # Highlight current state
            if current < total and state == steps[current][0]:
                if current < total-1:
                    dfa_graph.node(state, style='filled', fillcolor='lightblue', color='blue', penwidth='2')
                else:
                    dfa_graph.node(state, style='filled', fillcolor='lightgreen', color='blue', penwidth='2')
            else:
                dfa_graph.node(state)

        dfa_graph.attr('node', shape='plaintext')
        dfa_graph.node('start', label='')
        dfa_graph.edge('start', initial)            

        # Highlight current transition
        for (from_s, sym), to_s in transition_set.items():
            if current < total and steps[current] == (from_s, sym, to_s): 
                if current < total - 1:
                    dfa_graph.edge(from_s, to_s, label=sym, color='green', penwidth='2')
                else: 
                    dfa_graph.edge(from_s, to_s, label=sym)
            else:
                dfa_graph.edge(from_s, to_s, label=sym)

        dfa_graph.render('dfa', format='png', view=False)

        img = Image.open("dfa.png")
        photo = ImageTk.PhotoImage(img)
        dfa_label.config(image=photo)
        dfa_label.image = photo

        if current <= 0:
            prev_button.config(state="disabled")
        else:
            prev_button.config(state="normal")

        if current >= len(steps) - 1:
            next_button.config(state="disabled")
        else:
            next_button.config(state="normal")        
    
    # Next character in input string
    def next_transition():
        if step_index.get() < len(steps) - 1:
            step_index.set(step_index.get() + 1)
            symbol = steps[step_index.get()][1]
            dynamic_string.set(dynamic_string.get() + symbol)
            current_transition()

    # Previous character in input string
    def previous_transition():
        if step_index.get() > 0:
            step_index.set(step_index.get() - 1)
            dynamic_string.set(dynamic_string.get()[:-1])
            current_transition()

    string_label = tk.Label(displayer, text=f"String: '{input_str}'", font=("Arial", 10, "bold"))
    string_label.pack(pady=(10, 5))
    transition_label = tk.Label(displayer, text="Press next to begin", font=("Arial", 10))
    transition_label.pack(pady=(0, 10))
    current_label = tk.Label(displayer, text="", font=("Arial", 10))
    current_label.pack(pady=(0, 10))
    next_label = tk.Label(displayer, text="", font=("Arial", 10))
    next_label.pack(pady=(0, 10))

    # Back and forward buttons for window
    prev_button = tk.Button(displayer, text="Previous", command=previous_transition)
    prev_button.pack(side="left", padx=10)
    next_button = tk.Button(displayer, text="Next", command=next_transition)
    next_button.pack(side="right", padx=10)

    displayer.mainloop()

# Generate DFA button
def run():
    initial = initial_state.get().strip()
    states = [s.strip() for s in all_states.get().split(',')]
    alphabet_set = [a.strip() for a in alphabet.get().split(',')]
    accepting = set(a.strip() for a in accepting_states.get().split(','))

    transition_set = {}
    input=input_string
    for rule in transitions.get().split(';'):
        try:
            from_state, symbol, to_state = [part.strip() for part in rule.strip().split('-')]
            transition_set[(from_state, symbol)] = to_state
        except ValueError:
            result_label.config(text=f"Invalid transition format: '{rule}'", fg="red")
            return

    # Check for multiple initial states
    if initial.count(',') > 0:
        result_label.config(text="Only one initial state is allowed.", fg="orange")
        return

    # Check for missing transitions and add self-loops if requested
    missing_transitions = False
    for state in states:
        for symbol in alphabet_set:
            if (state, symbol) not in transition_set:
                result_label.config(text=f"Missing transition for state '{state}' on symbol '{symbol}'.", fg="orange")
                missing_transitions = True

    if missing_transitions:
        # Ask if missing transitions should be self loops
        response = messagebox.askyesno("Missing Transitions", "Do you want to add self-loops for missing transitions?")
        if response:
            # Update transition set with self loops for missing transitions
            for state in states:
                for symbol in alphabet_set:
                    if (state, symbol) not in transition_set:
                        transition_set[(state, symbol)] = state
            # Update input fields with self-loops added
            new_transitions = "; ".join([f"{from_state}-{symbol}-{to_state}" for (from_state, symbol), to_state in transition_set.items()])
            transitions.set(new_transitions)
            result_label.config(text="Self-loops added for missing transitions.", fg="green")
        return

    # Check for missing or incorrect accepting states
    accepting_states_list = accepting_states.get().split(',')
    accepting_states_list = [state.strip() for state in accepting_states_list]

    # Check if there are any empty accepting states
    if not accepting_states_list:
        result_label.config(text="No accepting state entered.", fg="orange")
        return

    # Check if all accepting states are valid (i.e., part of the states list)
    invalid_accepting_states = [state for state in accepting_states_list if state not in states]
    if invalid_accepting_states:
        result_label.config(text=f"Invalid accepting state(s): {', '.join(invalid_accepting_states)}.", fg="orange")
        return

    # Evaluate DFA with input string
    input_str = input_string.get().strip()
    current_state = initial

    # Tests input string
    if input_str:
        try:
            for symbol in input_str:
                if symbol not in alphabet_set:
                    raise ValueError(f"Symbol '{symbol}' not in alphabet.")
                current_state = transition_set[(current_state, symbol)]

            if current_state in accepting:
                result = f"Accepted! Ended in state: {current_state}"
                result_label.config(text=result, fg="green")  # Accepted in green
            else:
                result = f"Rejected. Ended in state: {current_state}"
                result_label.config(text=result, fg="red")  # Rejected in red

        except KeyError:
            result = f"Invalid transition from state '{current_state}' with symbol '{symbol}'"
            result_label.config(text=result, fg="red")  # Error in red
        except ValueError as ve:
            result_label.config(text=f"{ve}", fg="red")  # Error in red
    
    else:
        result_label.config(text="No input string provided", fg="orange")

    # Generate DFA visualization
    dfa_graph = graphviz.Digraph()

    for state in states:
        if state in accepting:
            dfa_graph.attr('node', shape='doublecircle')
        else:
            dfa_graph.attr('node', shape='circle')
        dfa_graph.node(state)

    dfa_graph.attr('node', shape='plaintext')
    dfa_graph.node('start', label='')
    dfa_graph.edge('start', initial)

    for (from_state, symbol), to_state in transition_set.items():
        dfa_graph.edge(from_state, to_state, label=symbol)

    dfa_graph.render('dfa', format='png', view=False)

    # Display DFA image in a new window
    output = tk.Toplevel()
    output.geometry("+800+100")
    # output.resizable(False, False)
    output.title("DFA OUTPUT")
    dfa_image = Image.open("dfa.png")
    dfa_photo = ImageTk.PhotoImage(dfa_image)
    dfa_label = tk.Label(output, image=dfa_photo)
    dfa_label.pack()

    output.mainloop()

# Sample run button
def sample_run():
    initial_state.set("q0")
    all_states.set("q0, q1")
    accepting_states.set("q1")
    alphabet.set("0, 1")
    transitions.set("q0-0-q1; q1-0-q0; q0-1-q0; q1-1-q1")
    input_string.set("011")

# Clear button
def clear():
    initial_state.set("")
    all_states.set("")
    accepting_states.set("")
    alphabet.set("")
    transitions.set("")
    input_string.set("")

# ------------------------------- Main GUI setup ------------------------------- #
root = tk.Tk()
root.title("DFA Visualizer")
root.config(padx=30, pady=30)
root.geometry("1000x500")

initial_state = tk.StringVar()
all_states = tk.StringVar()
alphabet = tk.StringVar()
transitions = tk.StringVar()
accepting_states = tk.StringVar()
input_string = tk.StringVar()

tk.Label(root, text="Use commas to separate multiple items (e.g., q0,q1,q2)", font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=(0, 10))

# GUI input fields and labels
tk.Label(root, text="Enter Initial State: ").grid(row=1, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=initial_state, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Enter All States: ").grid(row=2, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=all_states, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Alphabet: ").grid(row=3, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=alphabet, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Transitions (e.g. q0-0-q1; q1-0-q0): ").grid(row=4, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=transitions, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Enter Accepting State(s): ").grid(row=5, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=accepting_states, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Input String to Test: ").grid(row=6, column=0, padx=5, pady=5, sticky='w')
tk.Entry(root, textvariable=input_string, width=50, bd=2, relief="solid", highlightthickness=2).grid(row=6, column=1, padx=5, pady=5)

# Sample input button
tk.Button(root, text="Load Sample Inputs", command=sample_run).grid(row=7, column=0, columnspan=2, pady=10)
# Clear button
tk.Button(root, text="Clear", command=clear).grid(row=7, column=1, columnspan=2, pady=10, sticky='e')
# Generate DFA button
tk.Button(root, text="Generate DFA", command=run).grid(row=8, column=0, columnspan=2, pady=10)
# Visualize Transition button
tk.Button(root, text="Visualize Transitions", command=run_string).grid(row=9, column=0, columnspan=2, pady=10)

# Result label for showing messages
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()
