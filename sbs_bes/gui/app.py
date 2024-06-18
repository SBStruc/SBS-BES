import re
from pathlib import Path
import tkinter as tk
import sys
from tkinter import filedialog
from sbs_bes.build_beam_tables import main
from sbs_bes.extract_new_beam_dims import make_new_staad_file


def validate_input(*args):
    for arg in args:
        if not Path(arg).exists():
            return False
    return True


def runBESI():
    if not validate_input(
        template_file_var.get(),
        beam_forces_var.get(),
        beam_groups_var.get(),
        output_folder_var.get(),
    ):
        raise Exception("Some selected directories/files do not exist. Try again...")

    if re.match(r"[^A-Za-z0-9\-\_]+", output_file_var.get()):
        raise Exception("Invalid file name. Try again...")

    main(
        template_file_var.get(),
        beam_groups_var.get(),
        beam_forces_var.get(),
        output_file_var.get(),
        output_folder_var.get(),
    )


def make_new_staad_syntax():
    if not validate_input(
        beam_groups_var.get(),
        output_folder_var.get(),
    ):
        raise Exception("Some selected directories/files do not exist. Try again...")

    if re.match(r"[^A-Za-z0-9\-\_]+", output_file_var.get()):
        raise Exception("Invalid file name. Try again...")

    make_new_staad_file(
        beam_groups_var.get(),
        output_file_var.get(),
        output_folder_var.get(),
    )


def select_file(var, file_type):
    if file_type == "xlsm":
        allowed_types = [("Allowed Types", "*.xlsm")]
    elif file_type == "xlsx":
        allowed_types = [("Allowed Types", "*.xlsm")]
    elif file_type == "txt":
        allowed_types = [("Allowed Types", "*.txt")]
    else:
        allowed_types = None

    if allowed_types is not None:
        file_path = filedialog.askopenfilename(filetypes=allowed_types)
    else:
        file_path = filedialog.askopenfilename()
    var.set(file_path)


def select_folder(var):
    folder_path = filedialog.askdirectory()
    var.set(folder_path)


# Create the main window
root = tk.Tk()
root.maxsize(400, 500)
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
staad_output_folder_var = tk.StringVar()

# Widget 1: Beam Forces Text File
tk.Label(root, text="Template Excel File:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=template_file_var).grid(row=0, column=1, sticky="ew")
tk.Button(
    root, text="...", command=lambda: select_file(template_file_var, "xlsm")
).grid(row=0, column=2, sticky="w")
# Widget 2: Beam Forces Text File
tk.Label(root, text="Beam Forces Excel File:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=beam_forces_var).grid(row=1, column=1, sticky="ew")
tk.Button(root, text="...", command=lambda: select_file(beam_forces_var, "xlsx")).grid(
    row=1, column=2, sticky="w"
)

# Widget 3: Beam Groups Text File
tk.Label(root, text="STAAD Syntax Text File:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=beam_groups_var).grid(row=2, column=1, sticky="ew")
tk.Button(root, text="...", command=lambda: select_file(beam_groups_var, "txt")).grid(
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


tk.Label(root, text="New STAAD Syntax").grid(row=6, column=0, sticky="w", padx=10)

# Widget 7: Run button for creating updated STAAD syntax
tk.Button(root, text="Update STAAD Syntax", command=make_new_staad_syntax).grid(
    row=7, column=0, columnspan=3, pady=20
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
tk.Label(root, text="Console:").grid(row=8, column=0, sticky="w", padx=10)
console = tk.Text(root, height=10, width=50)
console["state"] = "disabled"
console.grid(row=9, column=0, columnspan=3, sticky="ew", padx=10)
console.tag_configure("stderr", foreground="#b22222")
sys.stdout = TextRedirector(console, "stdout")
sys.stderr = TextRedirector(console, "stderr")

tk.Label(root, text="").grid(row=10, column=0, sticky="w", padx=10)

# Run the application
root.mainloop()
