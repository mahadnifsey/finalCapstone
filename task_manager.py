#*** Task Manager ***
#*****************************************
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the ``
# program will look in your root directory for the text files.

# ===============================================================================================================
# Importing Libraries
# ====================
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Clear terminal
# ==============
def clear_terminal():
    # Fresh Terminal for user after option, similar to professional programs
    # Ref: https://www.geeksforgeeks.org/clear-screen-python/
    os.system('cls||clear')
# ===============================================================================================================
# ******************************************** Main Function Section ********************************************
# Generate new text files
# ========================
# Create new user file if it doesnt exist
def create_new_user_file():
# If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

# Create tasks file if it doesn't exist, using the pass in python method to avoid an error
def create_new_task_file():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

# Create Task Overview File if it doesn't exist...
def create_new_task_overview_file():
    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w") as default_file:
            pass

# Create Task Overview File if it doesn't exist...
def create_new_user_overview_file():
    if not os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "w") as default_file:
            pass

# Generate new Tasks
# ===================
# Function to create task list
# Reading the task text file, creating a list with each curent task having a dictionary
def generate_task_list():
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    # Define an empty task list
    t_list = []
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
        curr_t['completed'] = task_components[5] 

        t_list.append(curr_t)

    return t_list


# Login Section
# ===================
# Function that reads usernames and password data from the user.txt file stores as dictionary
def read_user_data_dict():
    # Split each individual line into a string
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Defining our empty dictionary, as we are using principles of abstraction we have to rename as it may cause conflict later
    user_pass = {}
    # Using a for loop to split key value pair into user & password
    for user in user_data:
        username, password = user.split(';')
        user_pass[username] = password

    # Returning our dictionary so we may use it later in the program
    return user_pass

#===============================================================================================================
# Defensive Program Function
# ==========================
# Choice Validation
# =================
# Function that ensures user input is validated and adds a layer of defene to our program
# Using the prinicples of abstraction, we can reuse this defensive function in multiple sections of our task manager
def choice_validation_defense(call, choicea, choiceb):
    # Initialise our variable state to False
    validated_option = False
    options = [choicea, choiceb]
    # Print request to the terminal for the user to see
    print(call)

    # Using a while loop we ensure that the user may only pick from the two choices presented
    while not validated_option:
        # Always capitalise the call entered by the user
        user_option_call = input(f"Choose from the options, {choicea} or {choiceb}: ").capitalize()
        
        # Using else/if statement, we either set the new variable state or print an error message
        if user_option_call in options:
            validated_option = True
        else:
            print("\nInvalid choice. Please try again.\n")

    # Return the users option
    return user_option_call

# Zero Division Error
# =================
#Division function: When a zero division error occurs (eg dividing by num_tasks when there are no tasks), 
#the variable is set to zero
def division(a,b):
    try:
        #NB: Create a function for this
        c = round(((a/b)*100),2)
        
    except ZeroDivisionError as error_1:
        c = 0.00
    
    return c

# Data Validation
# =================
def deadline_validation_defense():
    # Initialise our variable state to False
    validated_date = False
    # Variable to set to current date
    current_date = datetime.now()
    
    # Using a while loop we ensure that the correct date format is entered allowing user to try again
    while not validated_date:
        try:
            task_deadline = input("\nTask Deadline (YYYY-MM-DD): ")
            deadline = datetime.strptime(task_deadline, DATETIME_STRING_FORMAT)
        # Defensive program - print error message with explanation   
        except ValueError:
            print("\nInvalid datetime format. Ensure that the correct format is entered\n")
        
        # Using else/if statement, to avoid user entering a past date
        if deadline < current_date:
            print("\nYou must enter a date in the future. Please try again")
        else:
            validated_date = True
            # New Line
            print("\n")

    # Return the users option
    return deadline
#===============================================================================================================
# Update task files
# =================
# Function to overwrite text files that can be reused multiple times in our program
def update_task_files():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                t['completed'] 
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Printing Task files -  Which can be reused in our program
def print_task(list):
    display_str = "--------------------------------------------------------------------------\n"
    display_str += f"Task: \t\t\t {list[0]}\n"
    display_str += f"Assigned to: \t\t {list[1]}\n"
    display_str += f"Date Assigned: \t\t {list[2].strftime(DATETIME_STRING_FORMAT)}\n"
    display_str += f"Due Date: \t\t {list[3].strftime(DATETIME_STRING_FORMAT)}\n"
    display_str += f"Task Complete? \t\t {list[4]}\n"
    display_str += f"Task Description: \n {list[5]}\n"
    display_str += "--------------------------------------------------------------------------\n"
    print(display_str)

# ===============================================================================================================
# ******************************************** Login Section ****************************************************
# Login Function
def login():
    # Initialise our variable state to False
    logged_in = False

    # Defensive programming
    # We define a variable that we will use later that prevents the user to avoid a menu option loop
    Option_call = 0

    # Using a while loop to authenticate user access
    while not logged_in:
        # Using else/if statement if greater than 0
        if Option_call > 0:
            # Re-using our defensive program to allow user to attempt again
            re_validate = choice_validation_defense("For full access rights, ensure you login. Would you like to make another attempt?", "Y", "N")
            if re_validate == "N":
                print("\nLogin attempt failed!\n")
                break

        print("\nLOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        #Checking if user exists or not
        if curr_user not in username_password.keys():
            print("User does not exist. \n")
        #Checking if password matches
        elif username_password[curr_user] != curr_pass:
            print("Wrong password.\n")
        else:
            print("\nYou are logged in!")
            logged_in = True
        
        # Variable value will increase, allowing us to use it in the else/if statement
        Option_call += 1
    
    # Return our current variable state, and user
    return logged_in, curr_user

# ===============================================================================================================
# ******************************************** Menu Option Section ****************************************************
# Creating a menu function to easily manage which tasks admin or general users can access - abstraction
def menu_options():
    # Defining initial state as false
    initial_option = False
    # Create a list of all the available options to the user
    options = ["r", "a", "va", "vm", "gr", "ds", "cu", "e"]

    # Using a While loop we can ensure the user can only pick from our list of options
    while not initial_option:
        # Add Fresh Terminal here if not working at top - DELETE
        print(f"\nWelcome to Task Manager - User: {current_user}\n")
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

# ===============================================================================================================
# ******************************************** Registering User Section ******************************************
# Registering a new user Section
def reg_user():
    # Initialise our variable state to False
    new_reg_user = False

    # Using a while loop to add a defensive layer for user who want to stop registration
    while not new_reg_user:
        # Request user to enter username
        new_username = input("\nNew Username: ")
        # Request user to enter password 
        new_password = input("New Password: ")
        # Request user to enter password to confirm
        confirm_password = input("Confirm Password: ")

        # User exists using an else/if statement
        if new_username in username_password.keys(): 
            print("\nIt appears that this user already exists.\n")

            # Validation 
            #Ask the admin to attempt again using our variables from our login section of the program
            re_validate = choice_validation_defense("Would you like to make another attempt?", "Y", "N")

            # Fresh Start
            # If admin selects "N", the loop will break and returns to start of the entire program
            if re_validate == "N": 
                break
        else:
            # Check if the passwords match
            if new_password == confirm_password:
                # Successfull password match add password to current variable
                username_password[new_username] = new_password
                # Successfull password match print message
                print("\nNew user added\n")
                # Adding password variable to our user file
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                # We set our variable state to True if password is match
                new_reg_user = True
            
            # If the password does not match, the program loops again
            else:
                # Unsuccessfull password match message
                print("\nThe passwords you entered, do not match. Please try again!\n")
    
    clear_terminal()

# ===============================================================================================================
# ******************************************** Adding Task Section ****************************************************
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

    clear_terminal()

# ===============================================================================================================
# ******************************************** Viewing All Section ****************************************************
# Viewing all tasks Section
def view_all():
    clear_terminal()
    # Heading
    print("All Tasks\n")
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        
# ===============================================================================================================
# ******************************************** Viewing User Section ****************************************************
# Viewing (mine) tasks Section
def view_mine(curr_user):
    clear_terminal()
    # Heading
    # Using f string to be specific to user
    print(f"All {curr_user} Tasks\n")

    # Only print the tasks related to the user
    user_specific_task_list = print_user_specific_tasks_and_produce_list()

    # Using an else/if statement to identify if user has tasks or not
    if len(user_specific_task_list) == 0:
        print(f"{curr_user} has no tasks\n")
    else:
        # Request user to edit task (specific)
        user_task_edit_index, edit_request = user_task_selection(user_specific_task_list)

        # Mark Complete or edit again
        if edit_request:
            edit_user_specific_task(user_specific_task_list, user_task_edit_index,curr_user)

# Consolidating user specific tasks only using abstraction principles
def print_user_specific_tasks_and_produce_list():
    # Initialise the input
    request_number = 1
    #print user specific tasks and saving them to a list
    specific_task_list = []
    for t in task_list:
        if t['username'] == current_user:
            print(f"\n{current_user}: Task {request_number}")
            #creating a list containing elements for print_task function
            view_mine_print_list = [t['title'],t['username'],t['assigned_date'],t['due_date'],t['completed'],t['description']]
            print_task(view_mine_print_list)

            #This list stores a dictionary for each task the user has
            specific_task_list.append(t)
            request_number += 1

    return specific_task_list


# Edit user task Function
def user_task_selection(u_spec_task_list):
    # Initialise our variable state to False
    edit_number_validation = False

    # Using a while loop
    while not edit_number_validation:
    #Ensuring an incorrect data type is not entered
        try:    
            u_t_edit_index = int(input("How many tasks do you want to enter?\n(No task to enter, no problem, just enter -1 to return to the menu.): "))

        except ValueError as error:
            print(error)
            print("\nInvalid input. Please try again\n")
            continue

        if (u_t_edit_index >= 1) and (u_t_edit_index <= len(u_spec_task_list)):
            edit_number_validation = True
            edit_req = True
        elif (u_t_edit_index == -1):
            print("\nYou have selected to edit no tasks.\n")
            edit_number_validation = True
            edit_req = False
        else:
            print("\nInvalid entry. Please try again\n")

    #These variables are important for the next stages of the view_mine function
    return u_t_edit_index, edit_req


#Function dealing with all the variations when the user has requested to edit a task
def edit_user_specific_task(u_spec_t_list, task_to_edit_index,cur_user):
    user_change_task_input = choice_validation_defense("\n\nDo you wish to mark the task as complete or edit the task?\n", "Mark as complete", "Edit the task")
    #Get the task_list index for the task we wish to change 
    task_list_index = task_list.index(u_spec_t_list[task_to_edit_index - 1])

    if user_change_task_input == "Mark as complete":  
      
        task_list[task_list_index]['completed'] = "Yes"
        update_task_files()
        print("\nThe task has been marked as completed\n")
    else:                                   
        if task_list[task_list_index]['completed'] == "Yes": 
            print("\nThe task is already complete. You cannot edit the task. You will be returned to the options menu\n")
        else:    
                user_editing_choice = choice_validation_defense("\n\nDo you wish to change the user assigned to the task or the due date?\n", "Change user", "Change due date")
                        
                if user_editing_choice == "Change user": 
                    user_request_change_user_assigned_func(task_list_index,cur_user)
                else:                                       
                    user_requested_change_due_date_func(task_list_index)     


#Function when the user has requested to change the user assigned to one of their tasks
def user_request_change_user_assigned_func(index,cur_user):
    # Initialise our variable state to False
    user_validated = False

    while not user_validated:
        user_input_edit_user_assigned = input("\nEnter the name of the user you wish to assign this task to: ")

        if (user_input_edit_user_assigned in username_password.keys()) and (user_input_edit_user_assigned != cur_user):
            user_validated = True
        elif (user_input_edit_user_assigned in username_password.keys()) and (user_input_edit_user_assigned == cur_user):
            print("\nYou've entered your own username.\n")
            re_validate = choice_validation_defense("Do you wish to try again? You will return to the options menu otherwise", "Y", "N")
            if re_validate == "N": #if they don't wish to continue, the loop will break and the user sent back to the options menu
                break
        else:
            print("\nThe user does not exist in the database.\n")
            re_validate = choice_validation_defense("Do you wish to try again? You will return to the options menu otherwise", "Y", "N")
            if re_validate == "N": #if they don't wish to continue, the loop will break and the user sent back to the options menu
                break
                                
    if user_validated:
        task_list[index]['username'] = user_input_edit_user_assigned
        update_task_files()
        print("\nTask has been successfully edited.\n")


# Due Date Change to task
def user_requested_change_due_date_func(index):
    new_due_date = deadline_validation_defense()
    #New due date cannot be before the present date
    task_list[index]['due_date'] = new_due_date
    update_task_files()
    print("\nTask edited.\n")
    clear_terminal()

# ===============================================================================================================
# ******************************************** Display Statistics Section ****************************************

def display_stats():
    '''If the user is an admin they can display statistics about number of users
        and tasks, read from the overview text files. If the overview files are not found,
        then they are generated first, then read'''
    #If the two overview files don't exist, then call generate reports function
    if (not os.path.exists("task_overview.txt")) or (os.path.getsize("task_overview.txt") == 0):
        generate_reports()
    elif (not os.path.exists("user_overview.txt")) or (os.path.getsize("user_overview.txt") == 0):
        generate_reports()
    
    #Loop through the text files
    with open("task_overview.txt") as task_overview_file:
        for line in task_overview_file:
            #An empty line will contain "\n" only, which is 2 characters long
            #Any line with a length greater than 2 is not empty
            if len(line) > 2:
                print(line)
    
    #Create a gap
    print("\n\n")

    with open("user_overview.txt") as user_overview_file:
        for line in user_overview_file:
            if len(line) > 2:
                print(line)

# ===============================================================================================================
# ******************************************** Generate Report Section ****************************************

# Consolidate function to print multiple reports
def generate_reports():
    generate_task_overview()
    generate_user_overview()
    # 
    print("\nReports generated.\n")

# Generate Task 
def generate_task_overview():
    #Total_num tasks generated
    total_num_tasks_generated = len(task_list)
    #Now we must loop through the task list, to calculate the number of completed, uncomplete and overdue tasks
    num_completed_tasks = 0
    num_uncompleted_tasks = 0
    num_overdue_tasks = 0
    #To check if a task is overdue, we must compare it to the present date
    #https://www.geeksforgeeks.org/comparing-dates-python/
    present_date = datetime.now()
    for t in task_list:
        if t['completed'] == "Yes": #Condition 1: If task is marked as completed
            num_completed_tasks += 1
        else:   #Condition 2: If the task is marked as uncompleted
            num_uncompleted_tasks += 1
            #Any task overdue by definition must also be uncompleted
            if t['due_date'] < present_date: #Check if the task is overdue
                num_overdue_tasks += 1 
    
    #Calculate the two values using the division function
    percentage_tasks_incomplete = division(num_uncompleted_tasks, total_num_tasks_generated)
    percentage_tasks_overdue = division(num_overdue_tasks, total_num_tasks_generated)
    
    #Writing the data to the text file, creating the file if it didn't exist.
    # generate_empty_txt_file("task_overview.txt")
    create_new_task_overview_file()
    
    #Writing to the task_overview text file
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("==========================================\n")
        task_overview_file.write("\t\tTASK OVERVIEW\n\n")
        task_overview_file.write(f"Total number of tasks generated = {total_num_tasks_generated}\n\n")
        task_overview_file.write(f"Total number of completed tasks = {num_completed_tasks}\n")
        task_overview_file.write(f"Total number of uncompleted tasks = {num_uncompleted_tasks}\n")
        task_overview_file.write(f"Total number of overdue tasks = {num_overdue_tasks}\n\n")
        task_overview_file.write(f"Percentage of tasks incomplete = {percentage_tasks_incomplete} %\n")
        task_overview_file.write(f"Percentage of tasks overdue = {percentage_tasks_overdue} %\n")
        task_overview_file.write("==========================================\n")

# User Overview Function
def generate_user_overview():
    #Calculating some variables you wish to display
    total_num_users = len(username_password)
    total_num_tasks_generated = len(task_list)
           
    #Creating the text file if it doesn't exist
    # generate_empty_txt_file("user_overview.txt")
    create_new_user_overview_file()
    
    #writing to the user_overview text file
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("=====================================================================\n")
        user_overview_file.write("\t\t\tUSER OVERVIEW\n\n")
        user_overview_file.write(f"Total number of users registered = {total_num_users}\n")
        user_overview_file.write(f"Total number of tasks generate = {total_num_tasks_generated}\n\n")

        for user in username_password:
            user_overview_file.write(f"{user} REPORT:\n")
            user_specific_report(user, total_num_tasks_generated, user_overview_file)
            user_overview_file.write("---------------------------------------------------------------------")
            user_overview_file.write("\n\n")
        
        user_overview_file.write("=====================================================================\n")

# User Specific Report
#Generating the user specfic reports for the generate_user_overview function
def user_specific_report(a_user, tot_num_tasks, u_file):
    #Now we must loop through the task list, to calculate the number of completed, uncomplete and overdue tasks
    user_total_num_tasks = 0
    user_num_completed_tasks = 0
    user_num_uncompleted_tasks = 0
    user_num_overdue_tasks = 0
    present_date = datetime.now()

    #Looping through the task lists, using conditions to calculate some variables we wish to display
    for t in task_list:
        if t['username'] == a_user:
            user_total_num_tasks += 1
            if t['completed'] == "Yes": #Condition 1: If task is marked as completed
                user_num_completed_tasks += 1
            else:   #Condition 2: If the task is marked as uncompleted
                user_num_uncompleted_tasks += 1
            #Any task overdue by definition must also be uncompleted
                if t['due_date'] < present_date: #Check if the task is overdue
                    user_num_overdue_tasks += 1 

    #Calculating some variables you wish to display, excepting zero division errors
    percentage_total_tasks_assigned_to_user = division(user_total_num_tasks, tot_num_tasks)
    percentage_user_tasks_completed = division(user_num_completed_tasks, user_total_num_tasks)
    percentage_user_tasks_uncompleted = division(user_num_uncompleted_tasks, user_total_num_tasks)
    percentage_user_tasks_overdue = division(user_num_overdue_tasks, user_total_num_tasks)
    
    # Output writing Overview file
    u_file.write(f"Total number of tasks assigned to user = {user_total_num_tasks}\n")
    u_file.write(f"Percentage of total number of tasks assigned to user = {percentage_total_tasks_assigned_to_user} %\n")
    u_file.write(f"Percentage of tasks assigned that have been completed = {percentage_user_tasks_completed} %\n")
    u_file.write(f"Percentage of tasks assigned that must still be completed = {percentage_user_tasks_uncompleted} %\n")
    u_file.write(f"Percentage of tasks assigned that are overdue = {percentage_user_tasks_overdue} %\n")

# ===============================================================================================================
# ******************************************** Program Start Section ****************************************
# Task Manager Launch
# ====================
# Login Section
# Initiating user file function
create_new_user_file()

# generate_empty_txt_file("tasks.txt")
create_new_task_file()

# Assigning functions to variables, so we can reuse them
# New task Variable
task_list = generate_task_list()

# User data variable
username_password = read_user_data_dict()

# Login Section Function
login_status, current_user = login()

# Using an else/if statement to ensure the correct input is selected
if login_status:
    # We initialise the entry to something not avaulable in our options
    menu = "u"
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
        elif menu == 'ds': 
            if current_user == 'admin': 
                display_stats()
            else:
                print("You don't have authority to display the statistics. Please select another option\n")
        elif menu == "gr": 
            if current_user == 'admin': 
                generate_reports() 
            else:
                print("You don't have authority to generate reports. Please select another option\n") 
        # For Option "e", the program ends and prints message to the user.        
        else:
            print('\nThank you for using Task Manager!\n\n')