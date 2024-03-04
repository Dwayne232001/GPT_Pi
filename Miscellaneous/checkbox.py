import tkinter as tk

def print_value():
    print(speak_output.get())

root = tk.Tk()

speak_output = tk.BooleanVar()
speak_output.set(True)

checkbox = tk.Checkbutton(root, text="Test Checkbox", variable=speak_output, command=print_value)
checkbox.pack(pady=20)

root.mainloop()