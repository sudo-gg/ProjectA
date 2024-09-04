import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

db = sqlite3.connect("User_Data.db")
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Login_Information(ID INTEGER NOT NULL UNIQUE,
               Username TEXT NOT NULL UNIQUE,
               Password_Hash TEXT NOT NULL,
               PRIMARY KEY(ID AUTOINCREMENT))''')


# Functions
def nothingFunc():
    print("True")


def hashText(key):
    hashObject = hashlib.sha256()
    hashObject.update(key.encode('utf-8'))
    hashedText = hashObject.hexdigest()
    return hashedText


def checkPassword(password):
    number = False
    capital = False
    special = False
    # Length check
    if 3 < len(password) < 31:
        # Special character check
        for character in password:
            if 47 < ord(character) < 58:
                number = True
            elif 64 < ord(character) < 91:
                capital = True
            elif 96 < ord(character) < 123:
                pass
            else:
                special = True
        # Check all criteria has been met
        if number and capital and special:
            return True


def addToDb(username, password):
    # Username length check
    if 2 < len(username) < 20:
        if checkPassword(password):
            # If passed validation checks when make variable for the given username and replace spaces with underscores
            username = username.replace(" ", "_")
            # Using the hash function hash the password to be stored securely
            hashedPass = hashText(password)
            # Try to enter the information into the database but since the code doesn't know what is already in the db
            # Will have to receive the error from the database to then alert the user
            try:
                c.execute("INSERT INTO Login_Information(Username, Password_Hash) VALUES (?, ?)",
                          (username, hashedPass))
                db.commit()
                messagebox.showinfo("Sign Up Successful", "Account created successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Sign up Failed", "Username already taken")
        else:
            messagebox.showerror("Sign up Failed",
                                 "Password must be 4 or more and 30 or less characters and contain at least a "
                                 "special character,number and capital letter")
    else:
        messagebox.showerror("Sign up Failed", "Username must be 3 or more and 19 or less characters")


def func():
    print("True1")


def validateLogin(entryUsername, entryPassword, function):
    username = entryUsername
    hashedPass = hashText(entryPassword)
    # Presence check
    if username and entryPassword:
        c.execute('''SELECT Username,Password_Hash
        FROM Login_Information
        WHERE Username=? AND Password_Hash=?''', (username, hashedPass))
        # if the selected username and password exists then login success
        if c.fetchone():
            messagebox.showinfo("Login Successful", "Welcome!")
            print("True2")  # root.destroy()
            function()
        # the fetchone method will return none if no selecton has been made (if account doesn't exist)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    else:
        messagebox.showerror("Login Failed", "Enter a username and password")


def sign_up():
    # Will be a section of the login page so by making a Top level will close automatically when the login page is
    # closed
    rootSignUp = tk.Toplevel()
    rootSignUp.title("Sign Up Form")
    rootSignUp.geometry('300x150')
    # title
    labelTitle = tk.Label(rootSignUp, text="Sign In")
    labelTitle.pack()
    # Username label & entry
    usernameLabelSignUp = tk.Label(rootSignUp, text="Username:")
    usernameLabelSignUp.pack()
    usernameEntrySignUp = tk.Entry(rootSignUp)
    usernameEntrySignUp.pack()
    # Password label & entry
    passwordLabelSignUp = tk.Label(rootSignUp, text="Password:")
    passwordLabelSignUp.pack()
    passwordEntrySignUp = tk.Entry(rootSignUp)
    passwordEntrySignUp.pack()
    # Create sign-up button
    btn_signup = tk.Button(rootSignUp, text="Sign Up",
                           command=lambda: addToDb(usernameEntrySignUp.get(), passwordEntrySignUp.get()))
    btn_signup.pack()
    rootSignUp.mainloop()

sign_up()
