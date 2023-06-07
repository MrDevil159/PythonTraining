import traceback
import logging
import sqlite3
"""
  step 2: task manager with file operations

"""
task_list = []


def get_db_connection():
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    return conn, cursor


def create_table():
    conn, cursor = get_db_connection()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      description TEXT,
                      status TEXT
                      )''')
    conn.commit()
    conn.close()


def display_menu():
    print("Task manager menu:")
    # print("1. Add task")
    # print("2. View tasks")
    # print("3. Update task")
    # print("4. Delete task")
    # print("5. Exit")

    menu = {
        "1": "Add task",
        "2": "View tasks",
        "3": "Update task",
        "4": "Delete task",
        "5": "Exit",
        "6": "Load Tasks",
        "7": "Save tasks"
    }
    for item, value in menu.items():
        # print(item + ". " + value)
        print(f"{item}. {value}")
        # print("{0}. {1}".format(item, value))

def get_user_choice():
    choice = input("Enter your choice between 1 - 5: ") 
    return choice


def create_db_records(name, description, status):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)",
                       (name, description, status))
        conn.commit()
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()


def fetch_db_records(task_id):
    conn, cursor = get_db_connection()
    rows = []
    try:
        cursor.execute(f"select * from tasks where id={task_id}")
        rows = cursor.fetchall()
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
    return rows


def list_db_records():
    conn, cursor = get_db_connection()
    rows = []
    try:
        cursor.execute("select * from tasks")
        rows = cursor.fetchall()
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()
    return rows


def update_db_records(task_id, update_choice, value):
    conn, cursor = get_db_connection()
    try:
        if update_choice == "1":
            cursor.execute(
                f"update tasks set description='{value}' where id={task_id}"
            )
        else:
            cursor.execute(
                f"update tasks set status='{value}' where id={task_id}"
            )
        conn.commit()
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()


def delete_db_records(task_id):
    conn, cursor = get_db_connection()
    try:
        cursor.execute(
            f"delete from tasks where id={task_id}"
        )
        conn.commit()
    except Exception as e:
        logging.error(str(e))
        conn.rollback()
    finally:
        conn.close()


def add_task():
    # while True:
    #     task_id = input("Enter the task id: ")
    #     duplicate_id = any(task_id == task.get("id") for task in task_list)
    #     if duplicate_id:
    #         print("Id already exists; Please enter other value")
    #     else:
    #         break

    name = input("Please enter the task name: ")
    description = input("Please enter the task description: ")
    status = "TO_DO"
    create_db_records(
        name,
        description,
        status
    )
    # task_list.append(
    #     {
    #         "id": task_id,
    #         "name": name,
    #         "description": description,
    #         "status": status
    #     }
    # )


    print(f"Task added successfully: {name} - {status}")
    return True


def view_task():
    task_list = list_db_records()
    if not task_list:
        print("No tasks found")
    else:
        print("id | name | description | status")
        for task in task_list:
            task_id = task[0]
            task_name = task[1]
            description = task[2]
            status = task[3]
            print(f"{task_id} | {task_name} | {description} | {status}")
    return True


def update_task():
    task_id = input("Enter the task id ")
    task_id_exists = fetch_db_records(task_id)
    if not task_id_exists:
        print("Invalid task id")
        return True

    update_choice = ""
    while update_choice not in ["1", "2", "3"]:
        update_choice = input("What do you want to update? 1. Description 2. Status 3. Abort update ")
        if update_choice == "3":
            print("Update aborted")
            return True

    if update_choice == "1":
        description = input("Enter updated decription: ")
    else:
        status = input("Enter status: 1. TO_DO, 2. IN_PROGRESS, 3. COMPLETED ")
        if status == "1":
            status = "TO_DO"
        elif status == "2":
            status = "IN_PROGRESS"
        elif status == "3":
            status = "COMPLETED"
        else:
            print("Invalid status")
            return True

    update_db_records


    if update_choice == "1":
        update_db_records(
            task_id,
            update_choice,
            description
        )
    else:
        update_db_records(
            task_id,
            update_choice,
            status
        )

    print("Task updated")
    return True


def delete_task():
    task_id = input("Enter the task id ")
    task_id_exists = fetch_db_records(task_id)
    if not task_id_exists:
        print("Invalid task id")
        return True
    delete_db_records(task_id)
    print("Task deleted")
    return True


def save_tasks():
    filename = input("Enter the filename to save tasks: ")
    try:
        with open(filename, "w") as file:
            for task in task_list:
                file.write(f"{task['id']},{task['name']},{task['description']},{task['status']}\n")
        print("Tasks saved successfully.")
    except FileNotFoundError:
        print("File not found.")
    return True


def load_tasks():
    filename = input("Enter the filename to load tasks from: ")
    try:
        with open(filename, "r") as file:
            for line in file:
                name, description, status = line.strip().split(",")
                create_db_records(name, description, status)
            print("Tasks loaded successfully.")
    except FileNotFoundError:
        print("File not found.")
    
    return True


def exit_function():
    print("Thanks for using the task manager")
    return False


def invalid_choice():
    print("Invalid choice")
    return True


def main():
    try:
        create_table()
        display_menu()
        while True:
            choice = get_user_choice()
            # if choice == "1":
            #   pass
            # elif choice == "2":
            #   pass
            # elif choice == "3":
            #   pass
            # elif choice == "4":
            #   pass
            # elif choice == "5":
            #   print("Thanks for using the task manager")
            #   break
            # else:
            #   print("Invalid choice")

            choice_function_mapping = {
                "1": add_task,
                "2": view_task,
                "3": update_task,
                "4": delete_task,
                "5": exit_function,
                "6": load_tasks,
                "7": save_tasks
            }
            mapped_function = choice_function_mapping.get(choice)
            if not mapped_function:
                invalid_choice()
            else:
                conitnue = choice_function_mapping[choice] ()
                if not conitnue:
                    break
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())
        print("Something went wrong. Please try again")
main()