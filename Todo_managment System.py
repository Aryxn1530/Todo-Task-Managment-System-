import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import datetime
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Todo App")
        self.root.geometry("600x500")
        self.is_dark_mode = False

        self.tasks = []
        self.load_tasks()

        self.root.configure(bg="#f0f0f0")

        # --- Theme Toggle ---
        self.theme_button = ttk.Button(root, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(pady=5)

        # --- Frame for Inputs ---
        self.frame = ttk.Frame(root)
        self.frame.pack(pady=10)

        self.task_entry = ttk.Entry(self.frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.date_entry = DateEntry(self.frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(side=tk.LEFT, padx=5)

        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.frame, textvariable=self.category_var, width=10)
        self.category_menu['values'] = ("Work", "Study", "Personal", "Other")
        self.category_menu.set("Work")
        self.category_menu.pack(side=tk.LEFT, padx=5)

        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # --- Listbox ---
        self.tasks_listbox = tk.Listbox(root, width=80, height=15, font=("Arial", 12))
        self.tasks_listbox.pack(pady=10)
        self.tasks_listbox.bind('<Double-1>', self.edit_task)

        # --- Buttons ---
        self.mark_done_button = ttk.Button(root, text="Mark as Done", command=self.mark_done)
        self.mark_done_button.pack(pady=2)

        self.delete_button = ttk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=2)

        self.save_button = ttk.Button(root, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(pady=2)

        # --- Task Stats ---
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=5)

        self.update_tasks_listbox()

    def toggle_theme(self):
        if not self.is_dark_mode:
            self.root.configure(bg="#2e2e2e")
            self.tasks_listbox.configure(bg="#1e1e1e", fg="white")
            self.is_dark_mode = True
        else:
            self.root.configure(bg="#f0f0f0")
            self.tasks_listbox.configure(bg="white", fg="black")
            self.is_dark_mode = False

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            date = self.date_entry.get()
            category = self.category_var.get()
            timestamp = datetime.datetime.now().strftime("%H:%M %d-%m-%Y")
            full_task = f"[{category}] {task} (due {date}) (added {timestamp})"
            self.tasks.append(full_task)
            self.update_tasks_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            del self.tasks[index]
            self.update_tasks_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def mark_done(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            task = self.tasks[index]
            if "[Done]" not in task:
                self.tasks[index] = task + " [Done]"
                self.update_tasks_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to mark as done.")

    def edit_task(self, event):
        try:
            index = self.tasks_listbox.curselection()[0]
            old_task = self.tasks[index]
            new_task = self.task_entry.get().strip()
            if new_task:
                self.tasks[index] = new_task
                self.update_tasks_listbox()
                self.task_entry.delete(0, tk.END)
            else:
                self.task_entry.insert(0, old_task)
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to edit.")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)
        self.update_status()

    def update_status(self):
        total = len(self.tasks)
        completed = len([t for t in self.tasks if "[Done]" in t])
        self.status_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {total - completed}")

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for task in self.tasks:
                f.write(task + "\n")
        messagebox.showinfo("Saved", "Tasks saved to tasks.txt")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as f:
                self.tasks = [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()