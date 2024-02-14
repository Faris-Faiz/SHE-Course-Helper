import tkinter as tk
from tkinter import simpledialog
import subprocess
import os
from tkinter import messagebox
import subprocess

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Run Cron Script")
        self.create_widgets()

    def create_widgets(self):
        # Year input note
        tk.Label(self.root, text='2022 maksudnya 2022/2023 so kalau YEAR = 2012 maksudnya 2012/2013', 
                 wraplength=400, justify="left").grid(row=2, column=2)

        # User input
        tk.Label(self.root, text="User:").grid(row=0, column=0)
        self.user = tk.Entry(self.root)
        self.user.grid(row=0, column=1)

        # Password input
        tk.Label(self.root, text="Pass:").grid(row=1, column=0)
        self.password = tk.Entry(self.root, show="*")
        self.password.grid(row=1, column=1)

        # Year input
        tk.Label(self.root, text="YEAR:").grid(row=2, column=0)
        self.year = tk.Entry(self.root)
        self.year.grid(row=2, column=1)

        # Semester input
        tk.Label(self.root, text="SEM:").grid(row=3, column=0)
        self.semester = tk.Entry(self.root)
        self.semester.grid(row=3, column=1)

        # Submit button
        tk.Button(self.root, text="Submit", command=self.run_cron).grid(row=4, column=0, columnspan=2)

    def run_cron(self):
        user = self.user.get()
        password = self.password.get()
        year = self.year.get()
        semester = self.semester.get()

        # Check if any field is empty
        if not all([user, password, year, semester]):
            messagebox.showwarning("Warning", "All fields must be populated before running.")
            return

        # Create or overwrite the .env file with user, pass, YEAR, and SEM
        with open('.env', 'w') as env_file:
            env_file.write(f'user={user}\n')
            env_file.write(f'pass={password}\n')
            env_file.write(f'YEAR={year}\n')
            env_file.write(f'SEM={semester}\n')

        try:
            subprocess.run(['python', 'cron.py'], check=True)
            print("cron.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print("An error occurred while trying to execute cron.py:", str(e))
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        # Close the GUI window
        self.root.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()

if __name__ == "__main__":
    main()
