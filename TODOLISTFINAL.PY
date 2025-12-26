import tkinter as tk
from tkinter import ttk
from datetime import datetime

#task class
class Task:
    def __init__(self, name, scheduled_time=None, duration=None, priority="Medium"):
        self.name = name
        self.scheduled_time = scheduled_time  # None allowed
        self.duration = duration              # None allowed
        self.priority = priority
        self.created_at = datetime.now()
        self.completed = False
        self.completed_at = None

    def complete(self):
        self.completed = True
        self.completed_at = datetime.now()
#class in oops
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OOP Python To-Do Scheduler")
        self.root.geometry("850x780")

        self.active_tasks = []
        self.completed_tasks = []

        self.build_ui()
#main UI setup
    def build_ui(self):
        self.build_task_detail_panel()
        self.build_input_section()
        self.build_counters()
        self.build_active_tasks()
        self.build_completed_tasks()

    #scrolable task display pannel
    def build_task_detail_panel(self):
        frame = tk.LabelFrame(self.root, text="Selected Task Details")
        frame.pack(fill="both", padx=10, pady=5)

        text_frame = tk.Frame(frame)
        text_frame.pack(fill="both", expand=True)

        self.detail_text = tk.Text(text_frame, height=8, wrap="word")
        scrollbar = tk.Scrollbar(text_frame, command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=scrollbar.set)

        self.detail_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.detail_text.insert("end", "Click a task to view full details")
        self.detail_text.config(state="disabled")

    def show_task_details(self, task):
        self.detail_text.config(state="normal")
        self.detail_text.delete("1.0", "end")

        time_text = task.scheduled_time if task.scheduled_time else "No time"
        duration_text = f"{task.duration} hour(s)" if task.duration else "N/A"
        status = "Completed" if task.completed else "Active"

        text = (
            f"Task Name       : {task.name}\n"
            f"Scheduled Time : {time_text}\n"
            f"Duration       : {duration_text}\n"
            f"Priority       : {task.priority}\n"
            f"Status         : {status}\n"
            f"Created At     : {task.created_at.strftime('%H:%M')}\n"
        )

        if task.completed:
            text += f"Completed At   : {task.completed_at.strftime('%H:%M')}\n"

        self.detail_text.insert("end", text)
        self.detail_text.config(state="disabled")

    #the input segment
    def build_input_section(self):
        frame = tk.LabelFrame(self.root, text="Add New Task")
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Task Name *").grid(row=0, column=0)
        self.task_entry = tk.Entry(frame)
        self.task_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(frame, text="Scheduled Time (HH:MM)").grid(row=1, column=0)
        self.time_entry = tk.Entry(frame)
        self.time_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(frame, text="Duration (hours)").grid(row=2, column=0)
        self.duration_entry = tk.Entry(frame)
        self.duration_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(frame, text="Priority").grid(row=3, column=0)
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(
            frame,
            textvariable=self.priority_var,
            values=["Low", "Medium", "High"],
            state="readonly"
        ).grid(row=3, column=1, sticky="ew")

        tk.Button(frame, text="➕ Add Task", command=self.add_task).grid(
            row=4, column=0, columnspan=2, pady=5
        )

        frame.columnconfigure(1, weight=1)

   #creating counters
    def build_counters(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10)

        self.active_count = tk.Label(frame, text="Active Tasks: 0")
        self.active_count.pack(side="left")

        self.completed_count = tk.Label(frame, text="Completed Tasks: 0")
        self.completed_count.pack(side="right")
#creating scrolable active task
    def build_active_tasks(self):
        tk.Label(self.root, text="Active Tasks").pack()

        self.canvas = tk.Canvas(self.root, height=260)
        scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)

        self.active_container = tk.Frame(self.canvas)
        self.active_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.active_container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

   #completed task pannel
    def build_completed_tasks(self):
        tk.Label(self.root, text="Completed Tasks").pack()
        self.completed_container = tk.Frame(self.root)
        self.completed_container.pack(fill="both", expand=True, padx=10)

   #core program
    def add_task(self):
        name = self.task_entry.get().strip()
        time = self.time_entry.get().strip()
        duration = self.duration_entry.get().strip()
        priority = self.priority_var.get()

        if not name:
            return

        #creating Optional time
        if time:
            try:
                datetime.strptime(time, "%H:%M")
            except:
                return
        else:
            time = None

        #creating duration as optional 
        duration = int(duration) if duration.isdigit() else None

        task = Task(name, time, duration, priority)
        self.active_tasks.append(task)

        self.task_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

        self.refresh()

    def complete_task(self, task):
        task.complete()
        self.active_tasks.remove(task)
        self.completed_tasks.append(task)
        self.refresh()

    def delete_task(self, task):
        self.active_tasks.remove(task)
        self.refresh()
#sorting the task
    def sort_tasks(self):
        no_time = [t for t in self.active_tasks if t.scheduled_time is None]
        with_time = sorted(
            [t for t in self.active_tasks if t.scheduled_time],
            key=lambda t: t.scheduled_time
        )
        return no_time + with_time

  #refreshing UI
    def refresh(self):
        for w in self.active_container.winfo_children():
            w.destroy()
        for w in self.completed_container.winfo_children():
            w.destroy()

        for idx, task in enumerate(self.sort_tasks(), start=1):
            frame = tk.Frame(self.active_container, bd=1, relief="solid")
            frame.pack(fill="x", pady=2)

            time_text = task.scheduled_time if task.scheduled_time else "No time"

            label = tk.Label(
                frame,
                text=f"{idx}. [{time_text}] {task.name}",
                fg=self.priority_color(task.priority),
                anchor="w"
            )
            label.pack(side="left", fill="x", expand=True)
            label.bind("<Button-1>", lambda e, t=task: self.show_task_details(t))

            tk.Button(frame, text="✔", command=lambda t=task: self.complete_task(t)).pack(side="right")
            tk.Button(frame, text="🗑", command=lambda t=task: self.delete_task(t)).pack(side="right")

        for task in self.completed_tasks:
            tk.Label(
                self.completed_container,
                text=f"{task.name} ✔ at {task.completed_at.strftime('%H:%M')}",
                fg="gray"
            ).pack(anchor="w")

        self.active_count.config(text=f"Active Tasks: {len(self.active_tasks)}")
        self.completed_count.config(text=f"Completed Tasks: {len(self.completed_tasks)}")

    #utilisation
    def priority_color(self, priority):
        return {"High": "red", "Medium": "orange", "Low": "green"}[priority]

#running the program
root = tk.Tk()
TodoApp(root)
root.mainloop()

