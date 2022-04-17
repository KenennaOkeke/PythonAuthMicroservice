'''
Created April 16th, 2022
@author: Kenenna N. Okeke (https://kenenna.com)
@note: Python Auth Microservice Example - Client
'''

# Importations
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import json
import requests

loginEndpoint = 'http://127.0.0.1:8000/login' # Based off the py-server/web_py.py

root = tk.Tk()
root.title("Get Auth Token")

mainNotebook = ttk.Notebook(root) # Initialize the main notebook
mainNotebookMainTab = ttk.Frame(mainNotebook) # Initialize the main notebook's main tab
mainNotebookLoginTab = ttk.Frame(mainNotebook) # Initialize the main notebook's login tab


mainNotebook.add(mainNotebookMainTab, text ='HOME')
mainNotebook.add(mainNotebookLoginTab, text ='LOGIN')
mainNotebook.pack(expand = 1, fill ="both")

mainNotebook.tab(0, state="hidden")
mainNotebook.select(1)
mainNotebook.tab(1, state="normal")

ttk.Label( # Email/Username label
    mainNotebookLoginTab,
    text ="Email"
).grid(
    column = 0,
    row = 1,
    padx = 0,
    pady = 0,
    sticky='w'
)

loginUsername = tk.StringVar()
ttk.Entry( #username text box
    mainNotebookLoginTab,
    textvariable=loginUsername,
).grid(
    column = 0,
    row = 2,
    padx = 0,
    pady = 0,
    sticky="we",
)

#The Password Field
ttk.Label( #Password label
    mainNotebookLoginTab,
    text ="Password",
).grid(
    column = 0,
    row = 3,
    padx = 0,
    pady = 0,
    sticky='w'
)

loginPassword = tk.StringVar()
ttk.Entry( #password text box
    mainNotebookLoginTab,
    textvariable=loginPassword,
    show="*"
).grid(
    column = 0,
    row = 4,
    padx = 0,
    pady = 0,
    sticky="we",
)

ttk.Button( #the login button
    mainNotebookLoginTab,
    text="Login",
    command=lambda: login()
).grid(
    column = 0,
    row = 5,
    padx = 0,
    pady = 0,
    sticky="we",
)

user_token = ""
def login():
    r = requests.post(loginEndpoint, json=({
        'email': loginUsername.get(),
        'password' : loginPassword.get()
        })
    )
    data = json.loads(r.content)
    if(data["success"] == False):
        messagebox.showinfo("showinfo", (data["error"]))
    else:
        user_token = data["token"]
        mainNotebook.tab(0, state="normal")
        mainNotebook.select(0)
        mainNotebook.tab(1, state="hidden")

root.mainloop()