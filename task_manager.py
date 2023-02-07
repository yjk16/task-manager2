# This program can help small businesses manage tasks assigned to each member of a team.
# Had help from mentor Sashlin Moonsamy with sections vm and gr.
# Had help from my friend Silas with things including variable names, error handling and indentation.
# Had help from my friend Nick with things including scope and organisation.
# Watched Logan Meadows' live lecture replay on Capstone 2 and 3.
# Thabiso Mathebula's supplementary lectures helped me.
# Used a lot of googling. Sites include: codespeedy.com, geeksforgeeks.org and blog.finxter.com.

# Importing relevant libraries.
import datetime

# Defining global variables.
list_of_tasks = []
my_tasks_list = []


# Defining functions.
# This function will register a user.
def reg_user():
    if username == 'admin':
        new_username = input("\nPlease enter a username:\n").lower()

        while new_username in registered_usernames:
            new_username = input(
                "\nI'm afraid that username is already in use.  Please choose another username:\n").lower()

        new_password = input("\nPlease enter a password:\n").lower()
        password_confirmation = input("\nPlease confirm your password:\n").lower()

        while new_password != password_confirmation:
            new_password = input("\nYour passwords did not match.\nPlease try again.\nEnter a password:\n").lower()
            password_confirmation = input("\nPlease confirm your password:\n").lower()

        register_user = open("user.txt", "a")
        register_user.write(f"\n{new_username}, {new_password}")

        register_user.close()

    else:
        print("\nI'm afraid you don't have authority to access this area.")


# This function will add new tasks to tasks.txt.
def add_task():
    adding = open("tasks.txt", "a")

    username_of_task = input("\nPlease enter the username of the person whom the task is assigned to:\n").lower()
    title_of_task = input("\nWhat is the title of the task?\n")
    description_of_task = input("\nPlease give a description of the task:\n")
    date_today = datetime.datetime.now()
    date_assigned = date_today.strftime("%d %b %Y")
    due_date = input("\nWhat is the due date of the task?\n")
    task_complete = "No\n"

    adding.write(
        f"{username_of_task}, {title_of_task}, {description_of_task}, {date_assigned}, {due_date}, {task_complete}")

    adding.close()

# This function will start with an empty list, read the contents of tasks.txt, adding each task to the list
# and return the new list.
def tasks_list():
    task_file = open("tasks.txt", "r")

    task_list = []

    for line in task_file.readlines():
        line = line.strip().split(", ")

        # Assigning each task as a dictionary with keys on the left and the line index as values.
        task = dict(
            title=line[1],
            username=line[0],
            date_assigned=line[3],
            due_date=line[4],
            description=line[2],
            task_complete=line[5]
        )

        task_list.append(task)

    task_file.close()

    return task_list


# This function will display the task in a user-friendly manner.
def display_task(title_of_task, username_of_task, due_date, description_of_task):
    date_today = datetime.datetime.now()
    date_assigned = date_today.strftime("%d %b %Y")
    task_complete = "No\n"

    return f"\nTask:\t\t\t\t{title_of_task}\nAssigned to:\t\t{username_of_task}\nDate assigned:\t\t{date_assigned}\n" \
           f"Due date:\t\t\t{due_date}\nTask complete?\t\t{task_complete}" \
           f"Task description:\t{description_of_task}\n\n\t\t**********\n"


# This function will allow the user to view all tasks.
def view_all():
    list_of_tasks = tasks_list()

    for item in list_of_tasks:
        task_display = display_task(item['title'], item['username'], item['due_date'], item['description'])

        print(task_display)


# This function will allow the user to edit a file.
def edit_file(tasks_list):
    listing_tasks = tasks_list

    file = open("tasks.txt", "w")

    for each_task in listing_tasks:
        file.write(each_task['username'] + ', ' + each_task['title'] + ', ' + each_task['description'] + ', '
                   + each_task['date_assigned'] + ', ' + each_task['due_date'] + ', ' + each_task['task_complete'] + '\n')

    file.close()


# This function returns the number of lines in a file.
def total_lines(filename):
    txt_file = open(filename, "r")
    num = len(txt_file.readlines())
    txt_file.close()

    return num


# This function calculates the statistics for task overview and then writes them over to task_overview.txt.
def calculate_task_overview():
    count = 0
    overdue_count = 0

    tasks_file = open("tasks.txt", "r")

    for lines in tasks_file.readlines():
        line = lines.strip().split(", ")
        total_tasks = total_lines("tasks.txt")

        if line[5].lower() == 'yes':
            count += 1

        completed_tasks = count
        uncompleted_tasks = total_tasks - count
        date_today = datetime.datetime.now()
        due_date = datetime.datetime.strptime(line[4], "%d %b %Y")
        if line[5].lower() == 'no' and due_date < date_today:
            overdue_count += 1

        percentage_of_incomplete_tasks = round((uncompleted_tasks / total_tasks * 100), 2)
        percentage_of_overdue_tasks = round((overdue_count / total_tasks * 100), 2)

    tasks_file.close()

    task_overview_file = open("task_overview.txt", "w")

    task_overview_file.write("TASK OVERVIEW\n")
    task_overview_file.write(f"\nTotal number of tasks:\t\t\t\t\t\t\t{total_tasks}")
    task_overview_file.write(f"\nTotal number of completed tasks:\t\t\t\t{completed_tasks}")
    task_overview_file.write(f"\nTotal number of uncompleted tasks:\t\t\t\t{uncompleted_tasks}")
    task_overview_file.write(f"\nTotal number of overdue tasks:\t\t\t\t\t{overdue_count}")
    task_overview_file.write(f"\nPercentage of incomplete tasks:\t\t\t\t\t{percentage_of_incomplete_tasks}%")
    task_overview_file.write(f"\nPercentage of overdue tasks:\t\t\t\t\t{percentage_of_overdue_tasks}%")

    task_overview_file.close()


# This function calculates the statistics for user overview and then writes them over to user_overview.txt.
def calculate_user_overview():
    tasks = open("tasks.txt", "r")

    username_list = [line.split(", ")[0] for line in open("user.txt", "r").readlines()]

    contents = tasks.readlines()

    total_tasks = total_lines("tasks.txt")
    total_users = total_lines("user.txt")

    user_overview_file = open("user_overview.txt", "w")

    for user_info in username_list:
        count_user_tasks = 0
        count_user_completed = 0
        count_user_overdue = 0
        for line in contents:
            task = line.strip().split(", ")  # Each line as a list

            if user_info == task[0]:
                count_user_tasks += 1

                if task[5] == 'Yes':
                    count_user_completed += 1

                date_today = datetime.datetime.now()
                due_date = datetime.datetime.strptime(task[4], "%d %b %Y")
                if task[5].lower() == 'no' and due_date < date_today:
                    count_user_overdue += 1
            
        if count_user_tasks <= 0:
            print("\nThis user does not yet have any tasks assigned or there has been a mistake in your entry.")

        else:
            percentage_user_tasks = round((count_user_tasks / total_tasks * 100), 2)
            percentage_completed_user_tasks = round((count_user_completed / count_user_tasks * 100), 2)
            percentage_user_tasks_to_be_completed = 100 - percentage_completed_user_tasks
            percentage_user_overdue_tasks = round((count_user_overdue / count_user_tasks * 100), 2)

            user_overview_file.write(f"\nFor {user_info}:\n")
            user_overview_file.write(f"Total number of users recorded:\t\t\t\t\t{total_users}\n")
            user_overview_file.write(f"Total number of tasks recorded:\t\t\t\t\t{total_tasks}\n")
            user_overview_file.write(f"Total number of tasks assigned:\t\t\t\t\t{count_user_tasks}\n")
            user_overview_file.write(f"Percentage of total number of tasks assigned:"
                                     f"\t{percentage_user_tasks}%\n")
            user_overview_file.write(f"Percentage of completed tasks assigned:"
                                     f"\t\t\t{percentage_completed_user_tasks}%\n")
            user_overview_file.write(f"Percentage of tasks still to be completed:"
                                     f"\t\t{percentage_user_tasks_to_be_completed}%\n")
            user_overview_file.write(f"Percentage of overdue tasks:"
                                     f"\t\t\t\t\t{percentage_user_overdue_tasks}%\n")

    user_overview_file.close()
    
    tasks.close()


# This function presents the menu.
def menu():
    print("\nPlease select one of the options below...\n")
    print("r  - registering a user")
    print("a  - adding a task")
    print("va - view all tasks")
    print("vm - view my tasks")
    print("gr - generate reports")
    print("ds - display statistics")
    print("e  - exit")


# This is the log in section.
# It will check whether the user enters a valid username and password from those stored in the file user.txt.
username = input("\nPlease enter your username: \n").lower()
password = input("\nPlease enter your password: \n").lower()
registered_usernames = []
registered_passwords = []
login = open("user.txt", "r+")

for line in login.readlines():
    details = line.strip().split()
    registered_usernames.append(details[0].replace(",", ""))
    registered_passwords.append(details[1])

while username not in registered_usernames or password not in registered_passwords:
    username = input(
        "\nI'm afraid there was an error in your entry.\nPlease try again. \nPlease enter your username:\n").lower()
    password = input("\nPlease enter your password:\n").lower()

login.close()

while True:
    menu()
    choice = input("\nI choose:\n").lower()

    # If the user chooses option 'r', and that user has the username 'admin'
    # this section will allow the user to add a new username and password to those saved in user.txt.
    # It must first be confirmed that the username they have chosen is not already registered.
    # And that the password they have chosen has been input correctly twice.
    # If the user does not enter the username 'admin'
    # they will not be able to access this section and there will be a message to display this.
    if choice == 'r':
        reg_user()

    # If the user chooses 'a', they will be able to add tasks.
    # They will be asked to input the relevant data.
    # This data will then be stored in tasks.txt.
    elif choice == 'a':
        add_task()

    # In this section the user will be able to view all tasks.
    # The information will be imported from tasks.txt and displayed in a user-friendly manner.
    elif choice == 'va':
        view_all()

    # In this section the user will be able to view their own tasks.
    # The information will be imported from tasks.txt and displayed in a user-friendly manner and numbered.
    # If there are currently no tasks for the user in question, a relevant message will be displayed.
    elif choice == 'vm':
        task_file = open("tasks.txt", "r")

        my_task_list = []
        count = 1

        for line in task_file.readlines():
            line = line.strip().split(", ")

            # Assigning each task as a dictionary with keys on the left and the line index as values.
            task = dict(
                title=line[1],
                username=line[0],
                date_assigned=line[3],
                due_date=line[4],
                description=line[2],
                task_complete=line[5]
            )

            if username != task["username"]:
                continue

            my_task_list.append(task)

            my_task_display = display_task(task['title'], task['username'], task['due_date'], task['description'])
            my_tasks_displayed = str(count) + ". " + my_task_display

            print(my_tasks_displayed)

            count += 1

        task_file.close()

        # Here the user can find a specific task by entering a number, or return to the menu by entering -1.
        find_task = int(input(
            "\nPlease enter the number of the task that you wish to view or enter '-1' to return to the main menu:\n"))

        while find_task < -1 or find_task == 0 or find_task > len(my_task_list):
            find_task = int(input("\nI'm afraid your entry is invalid.\nPlease try again:\n"))

        if find_task == -1:
            continue

        # Assigning 'this_task' to match the number the user enters by using the index of my_task list.
        this_task = my_task_list[find_task - 1]

        print(display_task(this_task['title'], this_task['username'], this_task['due_date'], this_task['description']))

        completed = input("\nHas the task been completed? 'y' for 'yes' or 'n' for 'no':\n").lower()

        while completed != 'y' and completed != 'n':
            completed = input("\nThat was not one of the options.\nPlease try again...\n")

        # Here the user can mark a task as complete.
        if completed == 'y':
            if this_task['task_complete'] == 'Yes':
                print("\nThis task has already been completed!")

            else:

                all_tasks = tasks_list()
                this_task_index = all_tasks.index(this_task)
                this_task['task_complete'] = 'Yes'
                all_tasks[this_task_index] = this_task
                edit_file(all_tasks)

        else:
            # Here the user can edit the username of the task, or the due date.
            if this_task['task_complete'] == 'No':
                edit_task = int(input('''\nPlease select one of the options below:
    
                                   1. Edit the username of the task
                                   2. Edit the due date
                                   I choose...\n\t\t\t\t\t\t\t\t'''))

                if edit_task <= 0 or edit_task >= 3:
                    edit_task = int(input('''\nI'm afraid something has gone wrong.
                                           Please try again:
                                           1. Edit the username of the task
                                           2. Edit the due date
                                           I choose...\n\t\t\t\t\t\t\t\t'''))

                elif edit_task == 1:
                    edit_user = input("\nWhich username would you like to assign this task to?\n")

                    all_tasks = tasks_list()
                    this_task_index = all_tasks.index(this_task)
                    this_task['username'] = edit_user
                    all_tasks[this_task_index] = this_task
                    edit_file(all_tasks)

                elif edit_task == 2:
                    try:
                        new_due_date = input('''\nWhat is the new due date?
                        Please use the dd Mon yyyy format.
                        For example: 01 Jan 2023:\n\t\t\t\t\t\t\t\t''')

                        all_tasks = tasks_list()
                        this_task_index = all_tasks.index(this_task)
                        this_task['due_date'] = new_due_date
                        all_tasks[this_task_index] = this_task
                        edit_file(all_tasks)
                        break

                    except ValueError:
                        print("I'm afraid that was not a valid entry!")

            else:
                print("I'm afraid something has gone wrong!")

    # In this section, the statistics for task overview will be calculated and written over to task_overview.txt.
    # And the statistics for user overview will be calculated and written over to user_overview.txt.
    # They will only be available to view for the user 'admin'. (I thought as gr and ds are linked, this made sense.)
    elif choice == 'gr':
        if username == 'admin':
            calculate_task_overview()
            calculate_user_overview()

        else:
            print("\nI'm afraid you don't have authority to access this area.")
        
    # In this section, if the user is 'admin', they will be able to see the total number of tasks
    # and the total number of users displayed in a user-friendly manner.
    # If they are another user, they will be denied access.
    elif choice == 'ds':
        if username == 'admin':
    
            task_statistics = open("task_overview.txt", "r")

            print(task_statistics.read())

            task_statistics.close()
    
            user_statistics = open("user_overview.txt", "r")

            for info in user_statistics.readlines():
                stats_user = info.strip()

                print(stats_user)

            user_statistics.close()
    
        else:
            print("\nI'm afraid you don't have authority to access this area.")

    elif choice == 'e':
        print("\nThanks and have a good day!!!")
        exit()

    else:
        print("Something has gone wrong! Please try again.")
