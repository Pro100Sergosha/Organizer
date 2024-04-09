import csv
import os
from tabulate import tabulate
from styles import Styles
class ToDoApp:
    def __init__(self, user_id = None, user_mail = None, style_menu = Styles()):
        self.user_id = user_id
        self.style_menu = style_menu
        self.user_mail = user_mail
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


    def file_exists(self):
        return os.path.exists(self.file_path)


    def list_tasks(self):
        with open(self.file_path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = []
            tasks.extend(task for task in reader)
            return tasks

    def check_file_exists(self, file_path, fieldnames):
        if not os.path.exists(file_path):
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def show_tasks(self):
        self.check_file_exists(self.file_path, self.fieldnames)
        tasks = self.list_tasks()
        new_tasks = []
        for task in tasks:
            new_tasks.append([task["ID"],task["Task"], task["Completed"]])
        return tabulate(new_tasks, headers=["ID", "Task", "Completed"], tablefmt = self.style_menu.list_format())
   

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


    def todo_app_menu(self):
        if self.user_id == None:
            self.style_menu.new_print("You need to be logged in to access To-do application")
            return False
        else:
            self.style_menu.new_print(f"Logged in as {self.user_mail}")
        while True:
            self.style_menu.new_print("\nTask Management Menu")
            self.style_menu.new_print("1. Add a task")
            self.style_menu.new_print("2. Mark a task as completed")
            self.style_menu.new_print("3. Show all tasks")
            self.style_menu.new_print("4. Delete a task")
            self.style_menu.new_print("5. Return to main menu")

            choice = input("Choose an action: ")

            if choice == "1":
                list_tasks = []
                while True:
                    task = input("Enter the task or press ENTER to finish: ").strip()
                    if task == "":
                        for task in list_tasks:
                            self.save_task(task)
                        self.style_menu.new_print(self.show_tasks())
                        break
                    else:
                        list_tasks.append(task)
            elif choice == "2":
                if not self.file_exists():
                    self.style_menu.new_print("You need to add task first!")
                else:
                    self.style_menu.new_print(self.show_tasks())
                    task_id = input("Enter the task ID to mark as completed: ")
                    self.mark_task_completed(task_id)
            elif choice == "3":
                if not self.file_exists():
                    self.style_menu.new_print("You need to write your task first!")
                else:
                    self.style_menu.new_print(self.show_tasks())
            elif choice == "4":
                self.style_menu.new_print(self.show_tasks())
                task_id = input("Enter the task ID to delete: ").strip()
                if not self.file_exists():
                    self.style_menu.new_print("You need to write your task first!")
                elif task_id == "":    
                    self.style_menu.new_print("Task ID not found")
                else:
                    self.delete_task(task_id)
            elif choice == "5":
                self.style_menu.new_print("Returning to the main menu.")
                break
            else:
                self.style_menu.new_print("Invalid input. Please choose an action again.")
        
if __name__ == "__main__":
    app = ToDoApp()
    