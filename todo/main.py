import sys
import tasks


def print_menu():
    print("\n--- Todo List ---")
    print("1. Add Task")
    print("2. View Task")
    print("3. Toggle Complete")
    print("4. Edit Task")
    print("5. Delete Task")
    print("6. Exit")
    print("-------------------")


def handle_add() -> None:
    desc = input("Enter task description: ")
    if tasks.add_task(desc):
        print(f"Added: '{desc}'")
    else:
        print("Error: Task description cannot be empty")


def handle_view() -> None:
    current_tasks = tasks.get_tasks()
    if not current_tasks:
        print("No tasks found")
    else:
        print("\nTasks:")
        for i, task in enumerate(current_tasks, start=1):
            status = "[X]" if task["completed"] else "[ ]"
            print(f"{i}: {status} {task['title']}")


def handle_delete() -> None:
    handle_view()
    current_tasks = tasks.get_tasks()

    if current_tasks:
        choice = input("\nEnter number to delete: ")
        deleted_item = tasks.delete_task(choice)

        if deleted_item:
            print(f"Deleted: '{deleted_item}'")
        else:
            print("Error: Invalid task number")


def handle_toggle():
    handle_view()
    choice = input("\nEnter task number to toggle: ")
    completed = tasks.toggle_task(choice)
    if completed is not None:
        status = "COMPLETED" if completed else 'PENDING'
        print(f"Task is now {status}")
    else:
        print("Error: Invalid task number")


def handle_edit():
    handle_view()
    choice = input("\nEnter task number to edit: ")
    new_desc = input("Enter new description: ")
    title = tasks.edit_task(choice, new_desc)
    if title:
        print(f"Task updated to '{title}'")
    else:
        print("Error: Invalid input")


def main() -> None:
    while True:
        print_menu()

        choice = input("Select an option: ").strip()

        if choice == '1':
            handle_add()
        elif choice == '2':
            handle_view()
        elif choice == '3':
            handle_toggle()
        elif choice == '4':
            handle_edit()
        elif choice == '5':
            handle_delete()
        elif choice == '6':
            sys.exit(0)
        else:
            print("Invalid selection, please try again")


if __name__ == "__main__":
    main()
