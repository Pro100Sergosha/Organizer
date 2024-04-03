import csv
import os
from tabulate import tabulate
class ToDoApp:
    def __init__(self, user_id):
        self.user_id = user_id
        self.file_path = f"{user_id}'s_tasks.csv"
        self.fieldnames = ["ID", "Task", "Completed"]
        self.current_task_id = None
        self.current_directory = os.path.dirname(__file__)
        self.tasks_folder = os.path.join(self.current_directory, 'Tasks')
        self.file_path = os.path.join(self.tasks_folder, self.file_path)
    
    def save_task(self, task):
        if not os.path.exists(self.tasks_folder):
            os.makedirs(self.tasks_folder)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()
        
        task_id = 0
        if os.path.exists(self.file_path) and os.stat(self.file_path).st_size != 0:
            with open(self.file_path, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                ids = [int(row["ID"]) for row in reader]
                task_id = len(ids) + 1
        else:
            with open(self.file_path, "w") as file:
                task_id = 1
        with open(self.file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if os.stat(self.file_path).st_size == 0:
                writer.writeheader()
            writer.writerow({"ID": task_id, "Task": task, "Completed": False})
            print("Task successfully added with ID:", task_id)
        print(self.show_tasks())

    def file_exists(self):
        return os.path.exists(self.file_path)
        
    def list_tasks(self):
        with open(self.file_path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = []
            tasks.extend(task for task in reader)
            return tasks

    def show_tasks(self):
        tasks = self.list_tasks()
        new_tasks = []
        for task in tasks:
            new_tasks.append([task["ID"],task["Task"], task["Completed"]])
        return tabulate(new_tasks, headers=["ID", "Task", "Completed"])
   
    def check_task(self, task_id):
        tasks = self.list_tasks()
        task_exists = any(task["ID"] == task_id for task in tasks)
        return task_exists
    

    def mark_task_completed(self, task_id):
        tasks = []
        with open(self.file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            tasks.extend(task for task in reader)
            for task in tasks:
                if self.check_task(task_id):
                    if task["ID"] == task_id:
                        if task["Completed"] == "False":
                            task["Completed"] = "True"
                            break
                        else:
                            print("Task already complete")
                            return
                else:
                    print("Task id not found")

                    return

        with open(self.file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(tasks)
        print("Task with ID {} marked as completed.".format(task_id))


    def delete_task(self, task_id):
        tasks = self.list_tasks()
        if not self.check_task(task_id):
            print(f"Task with this ID not found.")
            return
        else:
            with open(self.file_path, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()
                for task in tasks:
                    if task["ID"] == task_id:
                        tasks.remove(task)
                writer.writerows(tasks)
            print(f"Task deleted.")

        
if __name__ == "__main__":
    app = ToDoApp()
    