import tkinter as tk
import sys
from tkinter import filedialog
from sbs_bes.build_beam_tables import main


def runBESI():
    # Placeholder for your function logic
    main(
        template_file_var.get(),
        beam_groups_var.get(),
        beam_forces_var.get(),
        output_file_var.get(),
        output_folder_var.get(),
    )


def select_file(var):
    file_path = filedialog.askopenfilename()
    var.set(file_path)


def select_folder(var):
    folder_path = filedialog.askdirectory()
    var.set(folder_path)


# Create the main window
root = tk.Tk()
root.maxsize(600, 400)
root.title("SBS-BESI v2.0")

# Configure column weights to center the content
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Create StringVars to hold the values of the widgets
template_file_var = tk.StringVar()
beam_forces_var = tk.StringVar()
beam_groups_var = tk.StringVar()
output_file_var = tk.StringVar()
output_folder_var = tk.StringVar()

# Widget 1: Beam Forces Text File
tk.Label(root, text="Template Excel File:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=template_file_var).grid(row=0, column=1, sticky="ew")
tk.Button(root, text="...", command=lambda: select_file(template_file_var)).grid(
    row=0, column=2, sticky="w"
)
# Widget 2: Beam Forces Text File
tk.Label(root, text="Beam ForcesTEST  Excel File:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=beam_forces_var).grid(row=1, column=1, sticky="ew")
tk.Button(root, text="...", command=lambda: select_file(beam_forces_var)).grid(
    row=1, column=2, sticky="w"
)

# Widget 3: Beam Groups Text File
tk.Label(root, text="STAAD Syntax Text File:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=beam_groups_var).grid(row=2, column=1, sticky="ew")
tk.Button(root, text="...", command=lambda: select_file(beam_groups_var)).grid(
    row=2, column=2, sticky="w"
)

# Widget 4: Output File Name
tk.Label(root, text="Output File Name:").grid(row=3, column=0, sticky="e")
tk.Entry(root, textvariable=output_file_var).grid(row=3, column=1, sticky="ew")

# Widget 5: Output Folder
tk.Label(root, text="Output Folder:").grid(row=4, column=0, sticky="e")
tk.Entry(root, textvariable=output_folder_var).grid(row=4, column=1, sticky="ew")
tk.Button(root, text="...", command=lambda: select_folder(output_folder_var)).grid(
    row=4, column=2, sticky="w"
)

# Widget 6: Run Button
tk.Button(root, text="Run", command=runBESI).grid(
    row=5, column=0, columnspan=3, pady=20
)


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", string, (self.tag,))
        self.widget.see(tk.END)  # Scroll to the end


# Widget 7: Text Box for Output
tk.Label(root, text="Console:").grid(row=6, column=0, sticky="w", padx=10)
console = tk.Text(root, height=10, width=50)
console["state"] = "disabled"
console.grid(row=7, column=0, columnspan=3, sticky="ew", padx=10)
console.tag_configure("stderr", foreground="#b22222")
sys.stdout = TextRedirector(console, "stdout")
sys.stderr = TextRedirector(console, "stderr")

# Run the application
root.mainloop()
