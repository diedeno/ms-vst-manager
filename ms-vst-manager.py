import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


"""
MuseScore VST manager
Copyright (c) 2025 Diego Denolf (graffesmusic)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


# Application Info
VERSION = "1.0"
LAST_MODIFIED = "2025-01-20"
LICENSE = "GPLv3"

# Determine JSON File Path Based on OS
def get_json_file_path():
    if os.name == 'nt':  # Windows
        return os.path.expandvars(r'%localappdata%\\MuseScore\\MuseScore4\\known_audio_plugins.json')
    elif os.name == 'posix':
        if "darwin" in os.sys.platform:  # macOS
            return os.path.expanduser('~/Library/Application Support/MuseScore/MuseScore4/known_audio_plugins.json')
        else:  # Linux
            return os.path.expanduser('~/.local/share/MuseScore/MuseScore4/known_audio_plugins.json')
    else:
        raise Exception("Unsupported OS")

json_file_path = get_json_file_path()

# Load JSON Data
if os.path.exists(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)
else:
    data = []

filtered_data = [{**item, "original_index": idx} for idx, item in enumerate(data)]

# Tkinter App Setup
root = tk.Tk()
root.title("MuseScore VST Manager")
root.geometry("1200x600")

# Style for Red Delete Text
style = ttk.Style()
style.configure("RedText.Treeview", foreground="red")

# Refresh Treeview with Updated Data
def refresh_treeview():
    for row in tree.get_children():
        tree.delete(row)

    for index, vst_data in enumerate(filtered_data):
        values = get_row_values(vst_data)
        tree.insert("", "end", iid=index, values=values, tags=("deletable",))

# Update the get_row_values function to use a Unicode ❌ symbol
def get_row_values(vst_data):
    category = vst_data.get("meta", {}).get("attributes", {}).get("categories", "Unknown Category")
    vst_id = vst_data.get("meta", {}).get("id", "Unknown ID")
    vendor = vst_data.get("meta", {}).get("vendor", "Unknown Vendor")
    path = vst_data.get("path", "Unknown Path")
    enabled = "✔" if vst_data.get("enabled", False) else "✘"
    error_code = vst_data.get("errorCode", None)
    error_code = "" if error_code == -1 or error_code is None else error_code  # Hide -1 or missing error codes
    return category, vst_id, vendor, path, enabled, error_code, "❌"

# Handle Delete Click
def handle_delete_click(event):
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)
    if column_id == "#7":  # The "Delete" column is column 7
        delete_entry(int(item_id))

# Refresh Treeview without row-level tags
def refresh_treeview():
    for row in tree.get_children():
        tree.delete(row)

    for index, vst_data in enumerate(filtered_data):
        values = get_row_values(vst_data)
        tree.insert("", "end", iid=index, values=values)

# Toggle Enabled Function
def toggle_enabled(event):
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)
    if column_id == "#5":  # The "Enabled" column is column 5
        index = int(item_id)
        vst_data = filtered_data[index]
        vst_data["enabled"] = not vst_data["enabled"]
        
        # Update the original data list
        original_index = vst_data["original_index"]
        data[original_index]["enabled"] = vst_data["enabled"]
        
        refresh_treeview()

# Define the delete_entry function
def delete_entry(index):
    """
    Deletes the entry at the given index after confirmation.
    """
    vst_name = filtered_data[index]["meta"].get("id", "Unknown ID")
    if messagebox.askyesno("Delete", f"Are you sure you want to delete '{vst_name}'?"):
        # Remove the original entry from the data
        original_index = filtered_data[index]["original_index"]
        del data[original_index]
        # Remove from filtered data and refresh
        del filtered_data[index]
        refresh_treeview()

# Handle Delete Click
def handle_delete_click(event):
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)
    if column_id == "#7":  # The "Delete" column is column 7
        delete_entry(int(item_id))

# Search Functionality
def search_treeview(query):
    global filtered_data
    query = query.lower()
    filtered_data = [
        vst for vst in data
        if query in vst.get("meta", {}).get("attributes", {}).get("categories", "").lower()
        or query in vst.get("meta", {}).get("id", "").lower()
        or query in vst.get("meta", {}).get("vendor", "").lower()
        or query in vst.get("path", "").lower()
    ]
    refresh_treeview()

# Sorting Functionality
sort_order = {}

def sort_treeview(column):
    global filtered_data
    reverse = sort_order.get(column, False)
    sort_order[column] = not reverse

    if column == "Enabled":
        filtered_data.sort(key=lambda x: x.get("enabled", False), reverse=reverse)
    elif column == "Error Code":
        filtered_data.sort(key=lambda x: x.get("errorCode", -1), reverse=reverse)
    else:
        column_map = {
            "Category": lambda x: x.get("meta", {}).get("attributes", {}).get("categories", ""),
            "ID": lambda x: x.get("meta", {}).get("id", ""),
            "Vendor": lambda x: x.get("meta", {}).get("vendor", ""),
            "Path": lambda x: x.get("path", ""),
        }
        filtered_data.sort(key=column_map[column], reverse=reverse)
    refresh_treeview()

# Backup Functionality
def backup_json():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = f"{json_file_path}_{timestamp}.bak"
    shutil.copy(json_file_path, backup_path)
    messagebox.showinfo("Backup", f"Backup created at {backup_path}")

# Save JSON Changes
def save_json():
    with open(json_file_path, "w") as file:
        # Save data with proper formatting
        json.dump(data, file, indent=2)
    messagebox.showinfo("Save", "Changes have been saved.")

# Create GUI Components
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

tree = ttk.Treeview(frame, columns=("Category", "ID", "Vendor", "Path", "Enabled", "Error Code", "Delete"), show="headings")
tree.heading("Category", text="Category", command=lambda: sort_treeview("Category"))
tree.heading("ID", text="ID", command=lambda: sort_treeview("ID"))
tree.heading("Vendor", text="Vendor", command=lambda: sort_treeview("Vendor"))
tree.heading("Path", text="Path", command=lambda: sort_treeview("Path"))
tree.heading("Enabled", text="Enabled", command=lambda: sort_treeview("Enabled"))
tree.heading("Error Code", text="Error Code", command=lambda: sort_treeview("Error Code"))
tree.heading("Delete", text="Delete")

tree.column("Category", width=150)
tree.column("ID", width=150)
tree.column("Vendor", width=150)
tree.column("Path", width=400)
tree.column("Enabled", width=100, anchor="center")
tree.column("Error Code", width=100, anchor="center")
tree.column("Delete", width=100, anchor="center")

tree.tag_configure("deletable", foreground="red")

tree.bind("<Double-1>", toggle_enabled)
tree.bind("<Button-1>", handle_delete_click)

tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Search Box
search_frame = ttk.Frame(root)
search_frame.pack(fill="x", pady=5)

search_label = ttk.Label(search_frame, text="Search:")
search_label.pack(side="left", padx=5)

search_entry = ttk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=5)

search_entry.bind("<KeyRelease>", lambda _: search_treeview(search_entry.get()))

# Button Panel
button_frame = ttk.Frame(root)
button_frame.pack(fill="x", pady=5)

backup_button = ttk.Button(button_frame, text="Backup", command=backup_json)
backup_button.pack(side="left", padx=5)

save_button = ttk.Button(button_frame, text="Save", command=save_json)
save_button.pack(side="left", padx=5)

exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)
exit_button.pack(side="right", padx=5)

footer = ttk.Label(root, text=f"Version: {VERSION} | Last Modified: {LAST_MODIFIED} | License: {LICENSE}")
footer.pack(side="bottom", pady=5)

# Initialize Treeview
refresh_treeview()
root.mainloop()

