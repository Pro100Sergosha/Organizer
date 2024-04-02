import csv
import os

class ToDoApp:
    def __init__(self, user_id):
        self.user_id = user_id
        self.filename = f"Tasks_{user_id}.csv"
        self.fieldnames = ["ID", "Task", "Completed"]

    def save_task(self, task):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()
        
        task_id = 0
        if os.path.exists(self.filename) and os.stat(self.filename).st_size != 0:
            with open(self.filename, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                ids = [int(row["ID"]) for row in reader]
                task_id = len(ids) + 1
        else:
            with open(self.filename, "w") as file:
                task_id = 1
        with open(self.filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if os.stat(self.filename).st_size == 0:
                writer.writeheader()
            writer.writerow({"ID": task_id, "Task": task, "Completed": False})
            print("Task successfully added with ID:", task_id)

        
    def list_tasks(self):
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = []
            for row in reader:
                tasks.append({"ID": row["ID"], "Task": row["Task"], "Completed": row["Completed"]})
            return tasks

    def mark_task_completed(self, task_id):
        tasks = self.list_tasks()
        task_found = False
        for task in tasks:
            if task["ID"] == task_id:
                task["Completed"] = True
                task_found = True
                break
        if not task_found:
            print("Task with ID  not found.".format(task_id))
            return
        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for task in tasks:
                writer.writerow(task)
        print("Task with ID {} marked as completed.".format(task_id))

    def delete_task(self, task_id):
        tasks = self.list_tasks()
        task_found = False
        updated_tasks = []
        for task in tasks:
            if task["ID"] == task_id:
                task_found = True
            else:
                updated_tasks.append(task)
        if not task_found:
            print(f"Task with ID {task_id} not found.")
            return
        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for task in updated_tasks:
                writer.writerow(task)
        print(f"Task with ID {task_id} deleted.")

if __name__ == "__main__":
    app = ToDoApp()
    app.save_task("Buy groceries")
