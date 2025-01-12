import os
import shutil
from datetime import datetime
from PIL import Image
import imagehash
import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import re

# Function to sanitize folder names
def sanitize_folder_name(name):
    return ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()

# Function to create folder structure
def create_folder_structure(base_path, year, month, file_type):
    year_folder = os.path.normpath(os.path.join(base_path, sanitize_folder_name(year)))
    month_folder = os.path.normpath(os.path.join(year_folder, sanitize_folder_name(month)))
    type_folder = os.path.normpath(os.path.join(month_folder, file_type))
    return type_folder

# Function to create Others folder
def create_others_folder(base_path):
    others_folder = os.path.normpath(os.path.join(base_path, 'Others'))
    return others_folder

# Function to create Duplicates folder
def create_duplicates_folder(base_path):
    duplicates_folder = os.path.normpath(os.path.join(base_path, 'Duplicates'))
    os.makedirs(duplicates_folder, exist_ok=True)
    return duplicates_folder

# Function to compute perceptual hash of an image
def compute_image_hash(file_path):
    try:
        with Image.open(file_path) as img:
            return str(imagehash.phash(img))
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

# Function to get file date based on user choice
def get_file_date(file_path, use_filename):
    if use_filename:
        try:
            # Extract date from filename using regex
            match = re.match(r'(\d{4})-(\d{2})-(\d{2})', os.path.basename(file_path))
            if match:
                return datetime.strptime(match.group(0), '%Y-%m-%d')
            else:
                return None
        except Exception as e:
            print(f"Error parsing filename date: {e}")
            return None
    else:
        try:
            return datetime.fromtimestamp(os.path.getctime(file_path))
        except FileNotFoundError:
            return None

# Function to arrange files by year and month
def arrange_files_by_date(folder_path, log_text, use_filename):
    others_folder = create_others_folder(folder_path)
    duplicates_folder = create_duplicates_folder(folder_path)
    seen_hashes = set()
    image_count = 0
    video_count = 0
    folder_count = 0
    duplicate_count = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            file_date = get_file_date(file_path, use_filename)
            if not file_date:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    image_folder = os.path.join(others_folder, 'Images')
                    os.makedirs(image_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(image_folder, filename))
                    log_text.insert(tk.END, f"Moved {filename} to {image_folder}\n")
                    image_count += 1
                elif filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.3gp')):
                    video_folder = os.path.join(others_folder, 'Videos')
                    os.makedirs(video_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(video_folder, filename))
                    log_text.insert(tk.END, f"Moved {filename} to {video_folder}\n")
                    video_count += 1
                else:
                    shutil.move(file_path, os.path.join(others_folder, filename))
                    log_text.insert(tk.END, f"Moved {filename} to {others_folder}\n")
                continue

            year = file_date.strftime('%Y')
            month = file_date.strftime('%B-%m')
            file_type = 'Images' if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) else 'Videos'

            target_folder = create_folder_structure(folder_path, year, month, file_type)
            if not os.path.exists(target_folder):
                folder_count += 1
            os.makedirs(target_folder, exist_ok=True)

            file_hash = compute_image_hash(file_path) if file_type == 'Images' else None

            if file_hash and file_hash in seen_hashes:
                shutil.move(file_path, os.path.join(duplicates_folder, filename))
                log_text.insert(tk.END, f"Moved duplicate {filename} to {duplicates_folder}\n")
                duplicate_count += 1
            else:
                if file_hash:
                    seen_hashes.add(file_hash)
                shutil.move(file_path, os.path.join(target_folder, filename))
                log_text.insert(tk.END, f"Moved {filename} to {target_folder}\n")
                if file_type == 'Images':
                    image_count += 1
                else:
                    video_count += 1

    log_text.insert(tk.END, f"\nSummary:\n")
    log_text.insert(tk.END, f"Images found: {image_count}\n")
    log_text.insert(tk.END, f"Videos found: {video_count}\n")
    log_text.insert(tk.END, f"Folders created: {folder_count}\n")
    log_text.insert(tk.END, f"Duplicates found: {duplicate_count}\n")

# Function to browse folder
def browse_folder(entry):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)

# Function to run the arrangement
def run_arrangement(entry, log_text, treeview, use_filename_var):
    folder_path = entry.get()
    if os.path.isdir(folder_path):
        log_text.delete(1.0, tk.END)
        use_filename = use_filename_var.get() == 1
        arrange_files_by_date(folder_path, log_text, use_filename)
        update_treeview(treeview, folder_path)

# Function to update the treeview
def update_treeview(treeview, folder_path):
    treeview.delete(*treeview.get_children())
    for root, dirs, files in os.walk(folder_path):
        for d in dirs:
            node = treeview.insert('', 'end', text=d, values=[os.path.join(root, d)])

# Function to open folder in file explorer
def open_folder(event):
    item = event.widget.selection()[0]
    folder_path = event.widget.item(item, 'values')[0]
    if os.path.isdir(folder_path):
        subprocess.Popen(f'explorer "{os.path.normpath(folder_path)}"')

# Create the GUI application
root = tk.Tk()
root.title("File Organizer")
icon_path = os.path.abspath('/<app_icon_path>/app_icon.ico')
root.iconbitmap(icon_path)
root.geometry("700x600")

# Frame for folder selection
frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=0, padx=10)

browse_button = tk.Button(frame, text="Browse", command=lambda: browse_folder(entry))
browse_button.grid(row=0, column=1)

use_filename_var = tk.IntVar()
filename_radiobutton = tk.Radiobutton(root, text="Use Filename Date", variable=use_filename_var, value=1)
filename_text = tk.Label(root, text = "(Ex: If filename '2015-09-16-xyz', then by this option a '2015' folder will create and then 'Setember-09' folder then 'Image' folder for images and 'Videos' foler for videos)" )
filename_text.bind('<Configure>', lambda e: filename_text.config(wraplength=filename_text.winfo_width(), justify="left"))
created_date_radiobutton = tk.Radiobutton(root, text="Use Created Date", variable=use_filename_var, value=0)
filecreated_text = tk.Label(root, text = "(By chossing of this option it'll create and arrange folder by file created date)" )
filecreated_text.bind('<Configure>', lambda e: filecreated_text.config(wraplength=filecreated_text.winfo_width(), justify="left"))
filename_radiobutton.pack(anchor="w", padx=20)
filename_text.pack(anchor="w", padx=20)
created_date_radiobutton.pack(anchor="w", padx=20)
filecreated_text.pack(anchor="w", padx=20)



run_button = tk.Button(root, text="Run File Organizer", command=lambda: run_arrangement(entry, log_text, treeview, use_filename_var))
run_button.pack(pady=10)

info_text = tk.Label(root, text = "Its supports - .png, .jpg, .jpeg, .bmp, .gif, .mp4, .mkv, .avi, .mov, .wmv, .3gp" )
info_text.bind('<Configure>', lambda e: info_text.config(wraplength=info_text.winfo_width(), justify="left"))
info_text.pack(anchor="w", padx=20)

# Log section
log_label = tk.Label(root, text="Log:", font=("Arial", 12, "bold"))
log_label.pack(anchor="w", padx=20)
log_text = tk.Text(root, height=10)
log_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

# Results section
results_label = tk.Label(root, text="Results:", font=("Arial", 12, "bold"))
results_label.pack(anchor="w", padx=20)

columns = ("Path",)
treeview = ttk.Treeview(root, columns=columns, show="tree")
treeview.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
treeview.bind("<Double-1>", open_folder)

root.mainloop()
