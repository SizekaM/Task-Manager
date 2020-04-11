# Library used to request the current date.
from datetime import date
import os.path
import datetime

#Main menu for actions to be carried out by logged in user.
def main_menu():
    if (login_username == "admin"):
        print("Please select one of the following options:")
        menu_options = input("r\t- \tRegister User\n"
                             "a\t- \tAdd Task\n"
                             "va\t- \tView All Tasks\n"
                             "vm\t- \tView My Tasks\n"
                             "gr\t- \tGenerate Reports\n"
                             "ds\t- \tDisplay Statistics\n"
                             "e\t- \tExit")

    else:
        print("Please select one of the following options:")
        menu_options = input("a\t- \tAdd Task\n"
                             "va\t- \tView All Tasks\n"
                             "vm\t- \tView My Tasks\n"
                             "s\t- \tView Statistics\n"
                             "e\t- \texit")

    if (menu_options != "r" and menu_options != "a" and menu_options != "va" and menu_options != "vm" and menu_options != "s" and menu_options != "e" and menu_options != "gr"):
        print("Invalid Option Selected")

        # Function for admin user to register a new user.
    if (menu_options == "r" and username == "admin"):
        reg_user()

        # Function for admin user to view statistucs.
    if (menu_options == "ds" and username == "admin"):
        statistics()

    if(menu_options == 'gr' and username == 'admin'):
        generate_reports()

        # Function used to add tasks that have to submitted for completion.
    if (menu_options == "a"):
        add_task()

        # Function used to view all tasks that have been submitted for completion.
    if (menu_options == "va"):
        view_all()

        # Prints the tasks assigned to a specific user
    if (menu_options == "vm"):
        view_mine()

        # Exits the program
    if (menu_options == "e"):
        print("Logging out...")

#Prompts user to either go back to main menu or close program
def return_menu():
    back_to_menu = input("Y: Back to main menu \nE: Log out").lower()

    while back_to_menu != 'e' and back_to_menu != 'y':
        menu_back = input("Invalid selection, back to the menu, N to exit? Y/N: ")

    if back_to_menu == 'e':
        print("Logging out...")
        exit()
    elif back_to_menu == 'y':
        main_menu()

#Creates a new user
def reg_user():
    print("\nRegistering a new user.")
    new_user = input("USERNAME:")
    with open('user.txt' , 'r') as f:
        for line in f:
            username, password = line.strip().split(', ')

            while(new_user == username):
                print("This username already exists!")
                new_user = input("USERNAME:")

    if (new_user != username):
        new_password = input("PASSWORD:")
        confirm_password = input("CONFIRM PASSWORD:")

        if (new_password == confirm_password):
            userfile.write(f"\n{new_user}, {new_password}")

        while(new_password != confirm_password):
            print("Paaswords are not a match. Try again!")
            new_password = input("PASSWORD:")
            confirm_password = input("CONFIRM PASSWORD:")

            if (new_password == confirm_password):
                userfile.write(f"\n{new_user}, {new_password}")
                print(f"{new_user} has succesfully been registered.")

#Creates a new task for any user
def add_task():
    with open('tasks.txt', 'r+') as taskfile:

        assigned_user = input("User Responsible For Task")
        task = input("Title of Task")
        description = input("Description of Task")
        assigned = date.today()
        due_date = input("Due date (YYYY-MM-DD)")
        task_complete = "No"
        taskfile.write(f"{task} \n{assigned_user} \n{description} \n{assigned} \n{due_date} \n{task_complete}")

#Creates Dictionary of tasks
def task_dict():
    with open('tasks.txt', 'r') as taskfile:
        task_dictionary = {}

        for i, line in enumerate(taskfile):
            values = line.strip().split(', ')

            task_dictionary[i + 1] = {
                                        'username': values[0],
                                        'task': values[1],
                                        'description': values[2],
                                        'date_assigned': values[3],
                                        'due_date': values[4],
                                        'task_complete': values[5]
                                       }

    return task_dictionary

#Creates dictionary of users
def user_dict():
    with open('user.txt', 'r') as userfile:
        user_dictionary = {}

        for i, line in enumerate(userfile):
            values = line.strip().split(', ')

            user_dictionary[i + 1] = {
                                        'username': values[0],
                                        'password': values[1],
                                    }

    return user_dictionary

#View all tasks
def view_all():
    task_dictionary = task_dict()

    for count in task_dictionary:
        task = task_dictionary[count]

        print(f"{count}) Task: \t\t\t{task['task']}")
        print(f"Assigned to: \t\t{task['username']}")
        print(f"Task description: \t{task['description']}")
        print(f"Date assigned: \t\t{task['date_assigned']}")
        print(f"Due date: \t\t\t{task['due_date']}")
        print(f"Task Complete?: \t{task['task_complete']}")
        print('')

        return_menu()

#View tasks assigned to specific user
def view_mine():

    task_dictionary = task_dict()
    found = False
    user_tasks = []

    for count in task_dictionary:
        task = task_dictionary[count]
        if username == task['username']:
            print(f"{count}) Task: \t\t{task['task']}")
            print(f"   Assigned to: \t{task['username']}")
            print(f"   Task description: \t{task['description']}")
            print(f"   Date assigned: \t{task['date_assigned']}")
            print(f"   Due date: \t\t{task['due_date']}")
            print(f"   Task Complete?: \t{task['task_complete']}")
            print('')
            user_tasks.append(count)
            found = True


        if not found:
            print(f"No tasks found for user {username}")

    user_choice = int(input("Key in task number to be edited."))

    while user_choice != 0 and user_choice not in user_tasks:
        user_choice = int(input(f"Task number for \"{username}\" does not exist, try again or type 0 to return to the menu: "))

    if user_choice != 0 and user_choice in user_tasks:
        edit_user_task(user_choice, task_dictionary)
    elif user_choice == 0:
        return_menu()

def edit_user_task(x, dictionary):
    print("TASK OPTIONS\n")
    print("1: Task Completion")
    print("2: Edit Task")
    print("3) Back to main menu\n")
    user_choice = input(f"Edit task ({x}) or mark as complete?: ")

    # Checking that the task isn't marked complete already
    # If it is, display the error, if not, mark as complete
    if user_choice == '1':
        if dictionary[x]['task_complete'] == 'Yes':
            print("Task already complete.")
        else:
            dictionary[x]['task_complete'] = 'Yes'
            print(f"Task \"{dictionary[x]['description']}\" is complete.")

    elif user_choice == '2':
        # Same error check as above
        if dictionary[x]['task_complete'] == 'Yes':
            print("Task already complete. No changes may be made.")
            return_menu()

        print("-==  Options  ==-\n")
        print(f"1) Change the user the task \"{dictionary[x]['description']}\" is assigned to")
        print(f"2) Change the due date for \"{dictionary[x]['description']}\"")
        print("3) Back to main menu\n")
        user_choice_change = input(f"Your choice?: ")

        if user_choice_change == '1':
            new_username = input(f"Please enter the new user to which the task \"{dictionary[x]['description']}\" will be assigned: ")
            dictionary[x]['username'] = new_username
        elif user_choice_change == '2':
                new_due_date = input(f"Please enter the new due date for task \"{dictionary[x]['description']}\": ")
                dictionary[x]['due_date'] = new_due_date
        elif user_choice == '3':
                return_menu()

    elif user_choice == '3':
            return_menu()

    with open('tasks.txt', 'w') as task_file:
        for count in dictionary:
            task_file.write(f"{dictionary[count]['username']}, {dictionary[count]['description']}, {dictionary[count]['task_note']}, {dictionary[count]['date_assigned']}, {dictionary[count]['due_date']}, {dictionary[count]['task_complete']}\n")

        return_menu()



# Display only admin specific statistics to the screen
def statistics():
    if not os.path.exists('task_overview.txt') and not os.path.exists('user_overview.txt'):
        generate_task_overview()
        generate_user_overview()

    print("\t\t Statistics\n")
    user_dictionary = user_dict()
    task_dictionary = task_dict()

    print(f"Total number of tasks: {len(task_dictionary)}")
    print(f"Total number of users: {len(user_dictionary)}")

    return_menu()


# Generate the task overview text file
def generate_task_overview():
    task_dictionary = task_dict()
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    # Open the file, creates it if it doesn't exist and reads each task from the task_dict function
    with open('task_overview.txt', 'w') as task_overview:
        for count in task_dictionary:
            task = task_dictionary[count]
            if 'Yes' == task['task_complete']:
                completed_tasks += 1
            elif 'No' == task['task_complete']:
                uncompleted_tasks += 1

            # Comparing the dates to check if the task is overdue
            datetime_object = datetime.datetime.strptime(task['due_date'], '%d %b %Y')
            if datetime_object < datetime.datetime.today() and 'No' == task['task_complete']:
                overdue_tasks += 1

        percentage_incomplete = (uncompleted_tasks * 100) / (len(task_dictionary))
        percentage_overdue = (overdue_tasks * 100) / (len(task_dictionary))

        task_overview.write(f"Total number of tasks generated using Task Manager: {len(task_dictionary)}\n")
        task_overview.write(f"Completed tasks: {completed_tasks}\n")
        task_overview.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview.write(f"Uncompleted tasks that are overdue: {overdue_tasks:.0f}\n")
        task_overview.write(f"Percentage of uncompleted tasks: {percentage_incomplete:.0f}%\n")
        task_overview.write(f"Percentage of uncompleted overdue tasks: {percentage_overdue:.0f}%\n")

        print("Task_overview.txt written.")


# Generate the user overview text file
def generate_user_overview():
    user_dictionary = user_dict()
    task_dictionary = task_dict()

# Reads each task from the task_dict function and users from the user_dict function
    with open('user_overview.txt', 'w') as user_overview:
        user_overview.write(f"Total number of users registered with Task Manager: {len(user_dictionary)}\n")
        user_overview.write(f"Total number of tasks generated using Task Manager: {len(task_dictionary)}")

        # Goes over each user
        for count in user_dictionary:
            tmp_user = user_dictionary[count]['username']

            task_counter = 0
            user_completed_tasks = 0
            user_uncompleted_tasks = 0
            overdue_tasks = 0
            for x in task_dictionary:
                task = task_dictionary[x]
                if tmp_user in task_dictionary[x]['username']:
                    task_counter += 1
                    if task['task_complete'] == 'Yes':
                        user_completed_tasks += 1
                    elif task['task_complete'] == 'No':
                        user_uncompleted_tasks += 1

                    # Compare due date to current date.
                    datetime_object = datetime.datetime.strptime(task['due_date'], '%d %b %Y')
                    if datetime_object < datetime.datetime.today() and 'No' == task['task_complete']:
                        overdue_tasks += 1

            # Calculates task percentages
            if user_completed_tasks > 0:
                percent_tasks_completed = (float(user_completed_tasks) * 100) / float(task_counter)
            elif user_completed_tasks == 0:
                percent_tasks_completed = 0

            if user_uncompleted_tasks > 0:
                percent_tasks_uncompleted = (float(user_uncompleted_tasks) * 100) / float(task_counter)
            elif user_uncompleted_tasks == 0:
                percent_tasks_uncompleted = 0

            if overdue_tasks > 0:
                percentage_overdue = (overdue_tasks * 100) / (user_uncompleted_tasks)
            elif overdue_tasks == 0:
                percentage_overdue = 0

            # Print everything to the file
            user_overview.write("\n")
            user_overview.write(f"\nTotal tasks assigned to user \"{tmp_user}\": {task_counter}\n")
            user_overview.write(
                f"Percentage of total number of tasks assigned to user \"{tmp_user}\": {(float(task_counter) * 100) / float(len(task_dictionary)):.2f}%\n")
            user_overview.write(
                f"Percentage of tasks assigned to user \"{tmp_user}\" completed: {percent_tasks_completed:.2f}%\n")
            user_overview.write(
                f"Percentage of tasks assigned to user \"{tmp_user}\" not completed: {percent_tasks_uncompleted:.2f}%\n")
            user_overview.write(
                f"Percentage of tasks assigned to user \"{tmp_user}\" not completed and are overdue: {percentage_overdue:.2f}%")

        print("User_overview.txt written.")


# Generate Reports for the admin user
def generate_reports():
    generate_task_overview()
    generate_user_overview()
    return_menu()







# Opens User file that  stores the usernames and passwords.
userfile = open('user.txt', 'r+')

# Reads the file assigned to userfile.
userfile.readlines()

login_username = input("USERNAME:")
login_password = input("PASSWORD:")
found_username = False

with open('user.txt', 'r+') as f:
    for line in f:
        username, password = line.strip().split(', ')

        # Function to check login details and signs in when the username and password are a match.
        if (login_username == username):
            found_username = True
            if(login_password == password):
                print(f"{login_username} is succesfully logged in\n")
                main_menu()

            else:
                print("Username or password is incorrect")

# Closes the user file that stores the username and password
userfile.close()
