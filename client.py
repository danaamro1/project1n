import tkinter as tk
from tkinter import ttk, messagebox
import requests

def send_request(url, method='GET', data=None, username=None, password=None):
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'PyBrowser'})
        response = None
        if method == 'GET':
            response = session.get(url, auth=(username, password), headers={'Cache-Control': 'max-age=3600'})
        elif method == 'POST':
            response = session.post(url, data=data, auth=(username, password))
        
        if response.status_code == 401:
            return "Authentication Required"
        elif response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return str(e)

def send_request_clicked():
    url = entry_url.get()
    method = method_var.get()
    data = entry_data.get() if method == 'POST' else None
    username = entry_username.get()
    password = entry_password.get()
    response = send_request(url, method, data, username, password)
    messagebox.showinfo("Response", response)

# Create main window
root = tk.Tk()
root.title("PyBrowser")

# Set background color
root.configure(bg="#ffc0cb")

# URL entry
label_url = tk.Label(root, text="URL:", bg="#ffc0cb")
label_url.grid(row=0, column=0, padx=5, pady=5)
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=5, pady=5)

# Method selection
label_method = tk.Label(root, text="Method:", bg="#ffc0cb")
label_method.grid(row=1, column=0, padx=5, pady=5)
method_var = tk.StringVar(root)
method_var.set("GET")
option_menu = ttk.Combobox(root, textvariable=method_var, values=["GET", "POST"])
option_menu.grid(row=1, column=1, padx=5, pady=5)

# Data entry for POST requests
label_data = tk.Label(root, text="Data (for POST):", bg="#ffc0cb")
label_data.grid(row=2, column=0, padx=5, pady=5)
entry_data = tk.Entry(root, width=50)
entry_data.grid(row=2, column=1, padx=5, pady=5)

# Username entry
label_username = tk.Label(root, text="Username:", bg="#ffc0cb")
label_username.grid(row=3, column=0, padx=5, pady=5)
entry_username = tk.Entry(root, width=50)
entry_username.grid(row=3, column=1, padx=5, pady=5)

# Password entry
label_password = tk.Label(root, text="Password:", bg="#ffc0cb")
label_password.grid(row=4, column=0, padx=5, pady=5)
entry_password = tk.Entry(root, width=50, show="*")
entry_password.grid(row=4, column=1, padx=5, pady=5)

# Send button
send_button = tk.Button(root, text="Send Request", command=send_request_clicked, bg="#007bff", fg="#fff")
send_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
