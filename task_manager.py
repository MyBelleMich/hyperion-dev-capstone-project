# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========

import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"
# Promp user to log in entering username and password
def login(username_password):       
    while True:
        username = input("Username: ")
        password = input("Password: ")
        if username in username_password and username_password[username] == password:
            print("Login successful!")
            return username
        else:
            print("Invalid username or password. Please try again.")

def reg_user(username_password):
    while True:  # Prompt user to enter a new username
        new_username = input("New Username: ").lower()  # Convert to lowercase

        # Check for duplicate usernames across the entire dictionary
        if any(username == new_username for username in username_password):
            print("This username already exists. Please try a different username.")
            continue

        new_password = input("New Password: ")  # Prompt user to add new and confirm password
        confirm_password = input("Confirm Password: ")

        if new_password == confirm_password:  # Check if passwords match
            print("New user added")
            username_password[new_username] = new_password  # Write the new username and password to the "user.txt" file 
            with open("user.txt", "a") as out_file:  # Open "user.txt" in append mode
                out_file.write(f"\n{new_username};{new_password}")  # Write to out_file
            break
        else:
            print("Passwords do not match")

def add_task(task_list, username_password):
    task_username = input("Name of person assigned to task: ") # Prompt user to enter name of person assigned to task
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")  # Prompt user to input title and description of task
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")  # Prompt user to input due date
            due_date_time = datetime.strptime(task_due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid datetime format. Please use the format shown.")

    curr_date = date.today()  # Get the current date

# Create a new_task dictionary with provided information
    new_task = {  
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "a") as task_file:  # Write the task details to the "tasks.txt" file, open in append mode
        str_attrs = [
            new_task["username"],
            new_task["title"],
            new_task["description"],
            new_task["due_date"].strftime(DATETIME_STRING_FORMAT),
            new_task["assigned_date"].strftime(DATETIME_STRING_FORMAT),
            "No"  
        ]
        task_file.write(";".join(str_attrs) + "\n")
    print("Task successfully added.")

def load_users():
    username_password = {}  # Create an empty dictionary to store username_password
    if os.path.exists("user.txt"):  # Check if user.txt exists
        with open("user.txt", "r") as user_file:  # open "user.txt" file in read mode as user_file
            user_data = user_file.read().split("\n")  # Read the contents of the file and split them into lines
            for user in user_data:  # Iterate over each line in the user data
                if user:
                    user_info = user.split(';')  # Split the line
                    if len(user_info) == 2:  # Check if length of user_info is equal to 2
                        username, password = user_info  # Confirm username and password
                        username_password[username] = password  # Add the username/password pair to the username_password dictionary
                    else:
                        print(f"Incorrect user data: {user}")
    return username_password  # Return the username_password pair

def load_tasks(username_password):
    task_list = []  # Create empty list to store task dictionary
    if os.path.exists("tasks.txt"):  # Check if tasks.txt exists
        with open("tasks.txt", "r") as task_file:  # If task exists open tasks.txt in read mode
            task_data = task_file.read().split("\n")  # read contents of file and split them into lines
            for t_str in task_data:
                if t_str:
                    curr_t = {}  # Create an empty dictionary to store task info
                    task_components = t_str.split(";")  # Split the line into task components then extract task details
                    curr_t["username"] = task_components[0]
                    curr_t["title"] = task_components[1]
                    curr_t["description"] = task_components[2]
                    curr_t["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
                    curr_t["assigned_date"] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
                    curr_t["completed"] = True if task_components[5] == "Yes" else False
                    task_list.append(curr_t)
    return task_list  # Return the list of task dictionaries

def view_all(task_list):  # Check if the task list is empty
    if not task_list:  # Print a message indicating no tasks available display_message
        print("No tasks available.")
        return
    
    print("All Tasks:")  # Print a header for all tasks
    for task in task_list:  # Iterate over each task in the task list
        print("=" * 60)  # Add this line to print the separator for the tasks
        print("Task Title:", task["title"])
        print("Assigned to:", task["username"])
        print("Due Date:", task["due_date"].strftime("%Y-%m-%d"))
        print("Task Description:", task["description"])
        print()

def view_my_task(task_list, curr_user):
    user_tasks = [task for task in task_list if task['username'] == curr_user]

    if not user_tasks:
        print(f"No tasks assigned to {curr_user}.")
        return

    print(f"Tasks assigned to {curr_user}:") # Print the task is assigned to the 'current user'
    for idx, task in enumerate(user_tasks, start=1): # Initialise an index counter
        print("=" * 60)  # Add this line to print the separator
        print(f"Task {idx}:")
        print("Task Title:", task["title"])
        print("Due Date:", task["due_date"].strftime("%Y-%m-%d"))
        print("Task Description:", task["description"])
        print("Status:", "Completed" if task["completed"] else "Incomplete")
        print()

    while True: # Loop for handling user input to edit or mark as complete
        choice = input("Enter the number of the task to edit, 'c' to mark as complete, or '-1' to return to the main menu: ")
        if choice == '-1':  # Check if the user wants to return to the main menu
            break  # Exit the loop
        elif choice == 'c':  
            task_num = int(input("Enter the number of the task to mark as complete: "))
            if 1 <= task_num <= len(user_tasks):
                selected_task = user_tasks[task_num - 1]
                if not selected_task["completed"]:
                    selected_task["completed"] = True
                    print(f"Task '{selected_task['title']}' marked as complete.")
                else:
                    print("Task is already marked as complete.")
            else:
                print("Invalid task number. Please try again.")
        elif choice.isdigit():  # Check if user input is a valid number
            task_num = int(choice)  # Convert user input to an integer
            if 1 <= task_num <= len(user_tasks):  # Check if entered number matches to a task
                selected_task = user_tasks[task_num - 1]  #Get the selected task from the task list
                if not selected_task["completed"]:
                    action = input("Enter 'username' to edit the assigned user, 'due date' to edit the due date, or '-1' to return to the main menu: ")
                    if action == '-1':  # Check the user action choice
                        break  # Exit the loop
                    elif action.lower() == 'username':  # Check if user wants to edit assigned user
                        new_username = input("Enter the new username for the task: ")  # Ask user for a new username
                        selected_task['username'] = new_username  # Update the task's assigned username
                        print("Username updated.")  # Print message to confirm update
                        break  # Exit loop
                    elif action.lower() == 'due date':  # Check if user wants to edit the due date
                        while True:  # Loop for validating new due date format
                            try:
                                new_due_date = input("Enter the new due date for the task (YYYY-MM-DD): ")
                                selected_task['due_date'] = datetime.strptime(new_due_date, "%Y-%m-%d") #Convert new due date string to a datetime object
                                print("Due date updated.")  # Print message to confirm update
                                break # Exit loop
                            except ValueError:  # Catch ValueError if the entered due date format is invalid
                                print("Invalid datetime format. Please use the format specified (YYYY-MM-DD)")  #Print error message
                                continue
                        break
                    else:
                        print("Invalid action. Please enter 'username', 'due date', or '-1'.") 
                else:
                    print("Task has already been completed and cannot be edited.")  # Print completed task message
            else:
                print("Invalid task number. Please try again.")  # Print invalid task number
        else:
            print("Invalid input. Please enter a number or '-1' to return to the main menu.")  # Print error message

def display_statistics(username_password, task_list):
    if os.path.exists("user.txt") and os.path.exists("tasks.txt"):  # Check if user.txt and tasks.txt exist
        print("***Displaying statistics***")  # Print message stating statistics are being displayed
        num_users = 0
        with open("user.txt", "r") as user_file:  # Open user.txt file in read mode
            for line in user_file:
                num_users += 1
        print(f"Number of Users: {num_users}")  # Print number of users

        num_tasks = 0
        with open("tasks.txt", "r") as task_file:  # Open tasks.txt file in read mode
            for line in task_file:
                num_tasks += 1
        print(f"Number of Tasks: {num_tasks}")

        completed_tasks = sum(1 for task in task_list if task['completed'])  # Count the number of completed tasks
        print(f"Number of Completed Tasks: {completed_tasks}") # Print number of completed tasks

        uncompleted_tasks = sum(1 for task in task_list if not task['completed'])  # Count the number of uncompleted tasks
        print(f"Number of Uncompleted Tasks: {uncompleted_tasks}")  # Print number of uncompleted tasks

        overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.today()) #Count the number of overdue tasks
        print(f"Number of Overdue Tasks: {overdue_tasks}")  # Print number of overdue tasks

        if num_tasks != 0:
            percentage_incomplete = (uncompleted_tasks / num_tasks) * 100
            print(f"Percentage of Incomplete Tasks: {percentage_incomplete:.2f}%")

            percentage_overdue = (overdue_tasks / num_tasks) * 100
            print(f"Percentage of Overdue Tasks: {percentage_overdue:.2f}%")
    else:
        print("Text files 'user.txt' and 'tasks.txt' not found. Generating reports...")  
        generate_reports(task_list, username_password)
        print("Reports generated. Please run the statistics again.")

        # Display generated reports
        print("\nDisplaying reports:")
        with open("user_overview.txt", "r") as user_overview_file:
            user_overview_data = user_overview_file.read()
            print("User Overview Report:")
            print(user_overview_data)

        with open("task_statistics.txt", "r") as task_stats_file:
            task_stats_data = task_stats_file.read()
            print("\nTask Statistics Report:")
            print(task_stats_data)

def generate_reports(task_list, username_password):
    # Calculate task Overview
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.today())
    
    total_users = len(username_password)  # Count total number of users
    tasks_assigned_to_users = {username: sum(1 for task in task_list if task['username'] == username) for username in username_password}  # Count tasks assigned to each user

# Write user overview report to file
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("=" * 60 + "\n")  # Add this line to print the separator
        user_overview_file.write("User Overview Report:\n")
        user_overview_file.write(f"Date and Time of Report: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        user_overview_file.write(f"Total Users: {total_users}\n")
        user_overview_file.write(f"Total Tasks: {total_tasks}\n\n")
        # Iterate over each user and their assigned tasks
        for username, task_count in tasks_assigned_to_users.items(): 
            completed_user_tasks = sum(1 for task in task_list if task['username'] == username and task['completed'])
            uncompleted_user_tasks = task_count - completed_user_tasks
            overdue_user_tasks = sum(1 for task in task_list if task['username'] == username and not task['completed'] and task['due_date'] < datetime.today())
            # Calculate percentages for different task statuses
            if task_count != 0:
                percentage_user_tasks = (task_count / total_tasks) * 100
                percentage_completed_user_tasks = (completed_user_tasks / task_count) * 100
                percentage_uncompleted_user_tasks = (uncompleted_user_tasks / task_count) * 100
                percentage_overdue_user_tasks = (overdue_user_tasks / task_count) * 100
            else:
                percentage_user_tasks = 0
                percentage_completed_user_tasks = 0
                percentage_uncompleted_user_tasks = 0
                percentage_overdue_user_tasks = 0
# Write user(specific) task statistics to file
            user_overview_file.write(f"User: {username}\n")
            user_overview_file.write(f"Total Tasks Assigned: {task_count}\n")
            user_overview_file.write(f"Percentage of Total Tasks: {percentage_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of Completed Tasks: {percentage_completed_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of Uncompleted Tasks: {percentage_uncompleted_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of Overdue Tasks: {percentage_overdue_user_tasks:.2f}%\n\n")
# Write task statistics to file
    with open("task_statistics.txt", "w") as task_stats_file:
        task_stats_file.write("=" * 60 + "\n")  # Add this line to print the separator
        task_stats_file.write("Task Statistics:\n")
        task_stats_file.write(f"Date and Time of Report: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        task_stats_file.write(f"Total Tasks: {total_tasks}\n")
        task_stats_file.write(f"Number of Completed Tasks: {completed_tasks}\n")
        task_stats_file.write(f"Number of Uncompleted Tasks: {uncompleted_tasks}\n")
        task_stats_file.write(f"Number of Overdue Tasks: {overdue_tasks}\n")
# Calculate & write percentages for incomplete and overdue tasks
        if total_tasks != 0:
            percentage_incomplete = (uncompleted_tasks / total_tasks) * 100
            task_stats_file.write(f"Percentage of Incomplete Tasks: {percentage_incomplete:.2f}%\n")

            percentage_overdue = (overdue_tasks / total_tasks) * 100
            task_stats_file.write(f"Percentage of Overdue Tasks: {percentage_overdue:.2f}%\n")

    print("Reports generated successfully.")

    # Prompt to display reports on screen
    display_reports = input("Do you want to display the reports on screen? (yes/no): ").lower()
    if display_reports == "yes":
        print("=" * 60)  # Add this line to print the separator
        print("\nUser Overview Report:")
        with open("user_overview.txt", "r") as user_overview_file:
            print(user_overview_file.read())
 # Print task statistics report
        print("=" * 60)  # Add this line to print the separator
        print("\nTask Statistics Report:")
        with open("task_statistics.txt", "r") as task_stats_file:
            print(task_stats_file.read())

def display_user_overview(task_list, username_password):
    # Calculate total number of tasks, completed, uncompleted and overdue tasks
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.today())
# Calculate percentages for incomplete and overdue tasks
    if total_tasks != 0:
        percentage_incomplete = (uncompleted_tasks / total_tasks) * 100
        percentage_overdue = (overdue_tasks / total_tasks) * 100
    else:
        percentage_incomplete = 0
        percentage_overdue = 0
# Count total number of users and tasks assigned to each user
    total_users = len(username_password)
    tasks_assigned_to_users = {username: sum(1 for task in task_list if task['username'] == username) for username in username_password}
    # Print user overview header
    print("User Overview:")
    print(f"Total Users: {total_users}")
    print(f"Total Tasks: {total_tasks}\n")

    # Iterate over each user and their assigned tasks
    for username, task_count in tasks_assigned_to_users.items():
        completed_user_tasks = sum(1 for task in task_list if task['username'] == username and task['completed'])
        uncompleted_user_tasks = task_count - completed_user_tasks
        overdue_user_tasks = sum(1 for task in task_list if task['username'] == username and not task['completed'] and task['due_date'] < datetime.today())
        
        # Calculate percentages for different task statuses
        if task_count != 0:
            percentage_user_tasks = (task_count / total_tasks) * 100
            percentage_completed_user_tasks = (completed_user_tasks / task_count) * 100
            percentage_uncompleted_user_tasks = (uncompleted_user_tasks / task_count) * 100
            percentage_overdue_user_tasks = (overdue_user_tasks / task_count) * 100
        else:
            percentage_user_tasks = 0
            percentage_completed_user_tasks = 0
            percentage_uncompleted_user_tasks = 0
            percentage_overdue_user_tasks = 0

        # Print user-specific task statistics
        print(f"User: {username}")
        print(f"Total Tasks Assigned: {task_count}")
        print(f"Percentage of Total Tasks: {percentage_user_tasks:.2f}%")
        print(f"Percentage of Completed Tasks: {percentage_completed_user_tasks:.2f}%")
        print(f"Percentage of Uncompleted Tasks: {percentage_uncompleted_user_tasks:.2f}%")
        print(f"Percentage of Overdue Tasks: {percentage_overdue_user_tasks:.2f}%\n")

    print("User overview report generated successfully.")

def main():
    # Welcome message
    print("Welcome to the Task Manager System!")
    username_password = load_users() # Load existing users from file
    username = login(username_password)  # Perform login 
    task_list = load_tasks(username_password)
    curr_user = username  # Set the current user to the logged-in user
# Menu options
    menu_options = """Select one of the following Options below:
    r - Register a user
    a - Add a task
    va - View all tasks
    vm - View my tasks
    ds - Display statistics
    """
# Add admin-specific menu option if the current user is admin they can access gr
    if curr_user == "admin":
        menu_options += "gr - Generate reports\n"
# Add exit option to the menu
    menu_options += "e - Exit\n"
# Main loop for user interaction
    while True:
        menu = input(menu_options).lower()
# Execute actions based on user input
        if menu == "r":
            reg_user(username_password)
        elif menu == "a":
            add_task(task_list, username_password)
        elif menu == "va":
            view_all(task_list)
        elif menu == "vm":
            view_my_task(task_list, curr_user)
        elif menu == "ds":
            display_statistics(username_password, task_list)
        elif menu == "gr" and curr_user == "admin":  # Only admin can generate reports
            generate_reports(task_list, username_password)
        elif menu == 'e':
            print("Goodbye!!!")
            exit() # Exit the program
        else:
            print("You've made a wrong choice, please try again")

if __name__ == "__main__":
    main()
