import tkinter as tk
from tkinter import messagebox
from backend import register_user, authenticate_user, get_user_id, store_password, retrieve_passwords
from db_setup import setup_database


def register():
    username = entry_username.get()
    password = entry_password.get()
    if register_user(username, password):
        messagebox.showinfo("Success", "User registered successfully.")
    else:
        messagebox.showerror("Error", "User already exists.")
        
def authenticate():
    username = entry_username.get()
    password = entry_password.get()
    if authenticate_user(username, password):
        messagebox.showinfo("Success", "User authenticated successfully.")
        user_id = get_user_id(username)
        store_password(user_id, entry_site.get(), entry_site_username.get(), entry_site_password.get(), password)
        messagebox.showinfo("Success", "Password stored successfully.")
        retrieved_passwords = retrieve_passwords(user_id, password)
        messagebox.showinfo("Retrieved Passwords", str(retrieved_passwords))
    else:
        messagebox.showerror("Error", "Invalid credentials.")
        
setup_database()

root = tk.Tk()
root.title("Password Manager")

tk.Label(root, text="Username").grid(row=0, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

tk.Label(root, text="Password").grid(row=1, column=0)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1)

tk.Label(root, text="Site").grid(row=2, column=0)
entry_site = tk.Entry(root)
entry_site.grid(row=2, column=1)

tk.Label(root, text="Site Username").grid(row=3, column=0)
entry_site_username = tk.Entry(root)
entry_site_username.grid(row=3, column=1)

tk.Label(root, text="Site Password").grid(row=4, column=0)
entry_site_password = tk.Entry(root, show="*")
entry_site_password.grid(row=4, column=1)

tk.Button(root, text="Register", command=register).grid(row=5, column=0)
tk.Button(root, text="Authenticate and Store Password", command=authenticate).grid(row=5, column=1)

root.mainloop()
