def add_task(task_name, status, tasks_dict):
    """
    Function adds a new task to the dictionary
    """
    tasks_dict[task_name] = status
    return tasks_dict

def remove_task(task_name, tasks_dict):
    """
    Function removes a task from the dictionary
    """
    if task_name in tasks_dict:
        del tasks_dict[task_name]
    return tasks_dict

def change_task_status(task_name, new_status, tasks_dict):
    """
    Function changes the status of an existing task
    """
    if task_name in tasks_dict:
        tasks_dict[task_name] = new_status
    return tasks_dict

def get_tasks_by_status(tasks_dict, status=None):
    """
    Function returns a list of tasks with the specified status
    If status is None, returns all tasks
    """
    if status is None:
        return list(tasks_dict.keys())
    return [task for task, task_status in tasks_dict.items() if task_status == status]

def display_tasks(tasks_dict, filter_status=None):
    """
    Displays tasks with optional filtering by status
    """
    # Filter tasks if a status filter is provided
    if filter_status:
        filtered_tasks = {task: status for task, status in tasks_dict.items() if status == filter_status}
    else:
        filtered_tasks = tasks_dict
    
    # If no tasks match the filter
    if not filtered_tasks:
        if filter_status:
            print(f"\nNo tasks with status '{filter_status}' found.")
        else:
            print("\nTask list is empty.")
        return
    
    # Display tasks in a table format
    print("\n" + "=" * 50)
    if filter_status:
        print(f"Tasks with status: {filter_status}")
    else:
        print("All Tasks")
    print("=" * 50)
    
    print(f"{'Task':<30} | {'Status':<15}")
    print("-" * 50)
    
    for task, status in filtered_tasks.items():
        print(f"{task:<30} | {status:<15}")
    
    print("-" * 50)
    print(f"Total: {len(filtered_tasks)} task(s)")

def interactive_task_management():
    """
    Interactive UI for task management system
    """
    # Initialize with some sample tasks
    tasks = {
        "Complete homework": "in progress",
        "Clean the room": "completed",
        "Call a friend": "pending",
        "Buy groceries": "pending",
        "Create a report": "in progress"
    }
    
    # Available task statuses
    valid_statuses = ["pending", "in progress", "completed"]
    
    while True:
        print("\nTask Management System")
        print("1. View All Tasks")
        print("2. View Tasks by Status")
        print("3. Add New Task")
        print("4. Remove Task")
        print("5. Change Task Status")
        print("6. Task Statistics")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            # View all tasks
            display_tasks(tasks)
            
        elif choice == "2":
            # View tasks by status
            print("\nAvailable statuses:")
            for idx, status in enumerate(valid_statuses, 1):
                print(f"{idx}. {status}")
            
            try:
                status_idx = int(input("\nEnter status number (or 0 to go back): "))
                if status_idx == 0:
                    continue
                
                if 1 <= status_idx <= len(valid_statuses):
                    selected_status = valid_statuses[status_idx - 1]
                    display_tasks(tasks, selected_status)
                else:
                    print("Invalid status number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "3":
            # Add new task
            task_name = input("\nEnter task name: ")
            
            if not task_name:
                print("Task name cannot be empty.")
                continue
                
            if task_name in tasks:
                print(f"Task '{task_name}' already exists.")
                continue
            
            print("\nAvailable statuses:")
            for idx, status in enumerate(valid_statuses, 1):
                print(f"{idx}. {status}")
                
            try:
                status_idx = int(input("\nEnter status number: "))
                
                if 1 <= status_idx <= len(valid_statuses):
                    selected_status = valid_statuses[status_idx - 1]
                    add_task(task_name, selected_status, tasks)
                    print(f"\nTask '{task_name}' added with status '{selected_status}'.")
                else:
                    print("Invalid status number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "4":
            # Remove task
            if not tasks:
                print("\nTask list is empty.")
                continue
                
            print("\nSelect a task to remove:")
            task_list = list(tasks.keys())
            for idx, task in enumerate(task_list, 1):
                print(f"{idx}. {task} ({tasks[task]})")
                
            try:
                task_idx = int(input("\nEnter task number (or 0 to cancel): "))
                if task_idx == 0:
                    continue
                    
                if 1 <= task_idx <= len(task_list):
                    task_to_remove = task_list[task_idx - 1]
                    confirm = input(f"Are you sure you want to remove '{task_to_remove}'? (y/n): ")
                    
                    if confirm.lower() == 'y':
                        remove_task(task_to_remove, tasks)
                        print(f"\nTask '{task_to_remove}' removed.")
                    else:
                        print("Removal cancelled.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "5":
            # Change task status
            if not tasks:
                print("\nTask list is empty.")
                continue
                
            print("\nSelect a task to change status:")
            task_list = list(tasks.keys())
            for idx, task in enumerate(task_list, 1):
                print(f"{idx}. {task} (Current status: {tasks[task]})")
                
            try:
                task_idx = int(input("\nEnter task number (or 0 to cancel): "))
                if task_idx == 0:
                    continue
                    
                if 1 <= task_idx <= len(task_list):
                    selected_task = task_list[task_idx - 1]
                    current_status = tasks[selected_task]
                    
                    print(f"\nCurrent status of '{selected_task}' is '{current_status}'")
                    print("\nSelect new status:")
                    
                    for idx, status in enumerate(valid_statuses, 1):
                        print(f"{idx}. {status}")
                        
                    status_idx = int(input("\nEnter new status number: "))
                    
                    if 1 <= status_idx <= len(valid_statuses):
                        new_status = valid_statuses[status_idx - 1]
                        
                        if new_status == current_status:
                            print(f"\nTask already has status '{new_status}'.")
                        else:
                            change_task_status(selected_task, new_status, tasks)
                            print(f"\nStatus of '{selected_task}' changed from '{current_status}' to '{new_status}'.")
                    else:
                        print("Invalid status number.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "6":
            # Task statistics
            if not tasks:
                print("\nTask list is empty.")
                continue
                
            total_tasks = len(tasks)
            
            # Count tasks by status
            status_counts = {}
            for status in valid_statuses:
                status_count = len(get_tasks_by_status(tasks, status))
                status_counts[status] = status_count
            
            # Display statistics
            print("\n" + "=" * 30)
            print("Task Statistics")
            print("=" * 30)
            print(f"Total Tasks: {total_tasks}")
            print("-" * 30)
            print(f"{'Status':<15} | {'Count':<5} | {'Percentage':<10}")
            print("-" * 30)
            
            for status, count in status_counts.items():
                percentage = (count / total_tasks) * 100 if total_tasks > 0 else 0
                print(f"{status:<15} | {count:<5} | {percentage:6.2f}%")
                
            print("=" * 30)
            
        elif choice == "7":
            # Exit
            print("Exiting Task Management System. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    # Run the interactive task management system
    interactive_task_management()
