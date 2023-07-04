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

#=======================================Main function Section=============================================
# A function to create task file - To add task_overview and user_overview files later - (add parameter)
# Create tasks.txt if it doesn't exist, using the pass in python method to avoid an error
def create_new_txt_file():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

#==============================================================================
# Function to create task list
# Reading the task text file, creating a list with each curent task having a dictionary
def create_task_list():
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    # Define an empty task list
    task_list = []
    # Using a for loop, looping through each line to be added to a dictionary called curr_t
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    # Return the new generated list task_list
    return task_list

#==============================================================================
#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
#=======================================================
# New User file Function?
def create_new_user_file():
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

#==============================================================================
# Reading usernames and password from the user.txt and writes to a dictionary called username_password
def create_username_password():
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

#==============================================================================
# Login Section - Login and while loop for non employees to exit
def login():
    # Defining initial login state as false
    logged_in = False
    while not logged_in:

        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    return logged_in, curr_user

#==============================================================================
# Menu Section
# ============
# Creating a menu function to easily manage which tasks admin or general users can access - abstraction
def menu_options():
    # Fresh Terminal for user after option, similar to professional programs
    # Ref: https://www.geeksforgeeks.org/clear-screen-python/
    os.system('cls') - # Delete: Add 'cls||clear' to argument if not working

    # Defining initial state as false
    initial_option = False
    # Create a list of all the available options to the user
    options = ["r", "a", "va", "vm", "gr", "ds", "cu", "e"]

    # Using a While loop we can ensure the user can only pick from our list of options
    while not initial_option:
        # Add Fresh Terminal here if not working at top - DELETE

        # presenting the menu_option to the user, ensuring input is lowercase
        # Variable menu was changed to menu_option to be used later in the program - abstraction
        menu_option = input('''Select one of the following Options below:
        r - Registering a user - (Admin)
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate Reports - (Admin)
        ds - Display statistics - (Admin)
        e - Exit
        : ''').lower()
        
        # Add a if else statement that breaks loops if option condition is selected.
        if menu_option in options:
            # The status of the initial option is changed only if input is a string
            print("")
            initial_option = True
        else:
            # Error message inlcuding new lines
            print("\nThis is an Invalid option. Please try again using only options shown\n")
    return menu_option

#==============================================================================
# Registering a new user Section
def reg_user():
	# Request user to enter username
    new_username = input("New Username: ")
    
    # Check if the username already exists using while loop
    while new_username in username_password:
		# Error message and prompt user to enter a new username
        print("Username already exists. Please choose a different username.")
        new_username = input("New Username: ")
    
	# Request user to enter a new password and confirm again
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

	# Using else/if statement to check if passwords match
    if new_password == confirm_password:
        # For console readability, new lines added to msg
        print("\nNew user added\n")
        username_password[new_username] = new_password
				# If successful user info is added to dictionary and text file
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

	# If user passwords do not match, error message is printed
    else:
        print("\nThis Passwords do not match! Please try again.\n")

# ====================================================================
# Adding a new task section
def add_task():
    # Definining initial variable status
    initial_new_task = False

    # Ensuring the validation of our username input by the user using a while loop
    while not initial_new_task:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        else:
            initial_new_task = True

    # User input of task and description
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # User input of the due date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get the current program date
    curr_date = date.today()

    # New task dictionary format
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }


    task_list.append(new_task)

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    print("\nTask successfully added.\n")

# ====================================================================
# Viewing all tasks Section
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
            
# ====================================================================
# Viewing current user tasks Section
def view_mine():
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)t
                
# ====================================================================
# Display statistics Section
def display_stats():
    if (not os.path.exists("task_overview.txt")) or (not os.path.exists("user_overview.txt")):
        generate_reports()

    with open("task_overview.txt", 'r') as task_file:
        task_data = task_file.read()
        print(task_data)
    with open("user_overview.txt", 'r') as user_file:
        user_data = user_file.read()
        print(user_data)
    input("Press any key to continue...")

#==============================================================================
# Task Manager Launch

# Login Section
login_status, curr_user = login()

#Ensure that only logged in employees can access + manipulate the data
if login_status:
    '''
    menu must be defined before we can have it as a condition for the while loop, 
    but we don't want it as any of the actual options
    '''
    menu = "x"
    '''Whilst the user has not selected the exit option, the loop continues, until the user
    selects the exit option ('e')
    As we have added to option to change the user, if they choose not to login again, the loop breaks
    and the program ends'''
    while menu != "e" and login_status:
        # presenting the menu to the user 
        menu = menu_options()

        if menu == 'r': #Change to admin only (Mentor suggestion)
            if current_user == 'admin': 
                reg_user() 
            else:
                print("You don't have authority to register a user. Please select another option\n")      
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            view_all()            
        elif menu == 'vm':
            view_mine(current_user)    
        elif menu == "gr": #Change to admin only
            if current_user == 'admin': 
                generate_reports() 
            else:
                print("You don't have authority to generate reports. Please select another option\n") 
        elif menu == 'ds' and curr_user == 'admin': 
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")    

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")