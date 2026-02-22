import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

#    custom modules
from ai_client import classify_file_sample
from db_client import ensure_table, insert_log
from config import CXX_SHREDDER_EXE, RISK_TO_LEVEL


selected_path = None 

def pick_file(path_var):
    path = filedialog.askopenfilename(title="Select file")
    if path:
        path_var.set(path)

def run_analyze(path_var, sector_var, cat_var, risk_var):
    path = path_var.get()
    if not path:
        messagebox.showwarning("Error", "Pick a file first!")
        return
    
# samplw
    with open(path, "rb") as f:
        sample = f.read(1024).decode(errors="ignore")
    
    cat, risk = classify_file_sample(sample, sector_var.get())
    cat_var.set(cat)
    risk_var.set(risk)

def run_shred(path_var, risk_var, cat_var):
    path = path_var.get()
    risk = risk_var.get()
    
#level???????????
    if risk >= 8: level_name = "Private"
    elif risk >= 5: level_name = "Internal"
    else: level_name = "Public"
    
    level = RISK_TO_LEVEL[level_name]
    
    try:
        #Cpp   Shredder
        result = subprocess.run([CXX_SHREDDER_EXE, path, str(level)], capture_output=True)
        ok = (result.returncode == 0)
        
        #azure
        ensure_table()
        insert_log(os.path.basename(path), cat_var.get(), risk, ok)
        messagebox.showinfo("Done", "Shredded and Logged to Azure!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

def build_ui():
    root = tk.Tk()
    root.title("Max's AI Shredder")
    root.geometry("500x400")

    path_var = tk.StringVar()
    sect_var = tk.StringVar(value="Furniture")
    cat_var = tk.StringVar(value="Unknown")
    risk_var = tk.IntVar(value=0)

    #ui :)
    tk.Label(root, text="Step 1: Select File").pack(pady=5)
    tk.Entry(root, textvariable=path_var, width=50).pack()
    tk.Button(root, text="Browse", command=lambda: pick_file(path_var)).pack()

    tk.Label(root, text="Step 2: Sector").pack(pady=5)
    tk.OptionMenu(root, sect_var, "Furniture", "Electronics", "Healthcare").pack()

    tk.Button(root, text="Step 3: AI Analyze", command=lambda: run_analyze(path_var, sect_var, cat_var, risk_var)).pack(pady=10)
    tk.Label(root, text="AI Category:").pack()
    tk.Label(root, textvariable=cat_var, fg="blue").pack()

    tk.Button(root, text="Step 4: SHRED", bg="red", fg="white", 
              command=lambda: run_shred(path_var, risk_var, cat_var)).pack(pady=20)

    return root

if __name__ == "__main__":
    app = build_ui()
    app.mainloop()