import json
import re
import datetime
import maskpass


db_file = "crowdfunding.json"

def save_data(data):
    with open(db_file, "w") as file:
        json.dump(data, file,indent=4)

def load_data():
    try:
        with open(db_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError):
        return {"users": [], "projects": []}

def register():
    data = load_data()
    fname = input("Enter your first name:\n\t")
    lname = input("Enter your last name:\n\t")
    while True:
        email = input("Enter your email:\n\t")
        if not re.match(r'^[a-zA-Z0-9_.]+@[a-z]+\.[a-z]{2,}$', email) :
            print("❌ Invalid email! Ensure the email follows a standard format (e.g., local@domain.com)\n")
            continue
        if any(user["email"] == email for user in data["users"]):
            print("❌ Email already exists! Enter another one\n")
            continue
        break 


    while True:
        password = maskpass.askpass(prompt='''Enter password that meets the following criteria:\n
                    - At least 8 characters long.\n
                    - Contains at least one uppercase letter.\n
                    - Contains at least one special character.\n
                    - Contains at least one digit.\n
                    ''', mask="*")


        password = password.strip()  

        if len(password) < 8:
            print("❌ Your password is too short! It must be at least 8 characters long.\n")
            continue
        if not re.search(r'[A-Z]', password):
            print("❌ Password must contain at least one uppercase letter.\n")
            continue
        if not re.search(r'\d', password):
            print("❌ Password must contain at least one digit.\n")
            continue
        if not re.search(r'[^a-zA-Z0-9]', password):  
            print("❌ Password must contain at least one special character.\n")
            continue
        else:
            break  
    while True:
        confirm_password = maskpass.askpass(prompt="Confirm Password:\n\t", mask="*")
        if password == confirm_password:
            print("Password confirmed successfully!")
            break
        print("❌ Passwords do not match! Please try again.")
    while True:
        phone = input("Enter your phone number:\n\t")
        if re.match(r"^01[0-9]{9}$", phone):
            break
        print("❌ Invalid phone number!")
    data["users"].append({"id":len(data["users"]),"fname": fname, "lname": lname, "email": email, "password": password, "phone": phone})
    save_data(data)
    print("✅ You registered successfully!")


def login():
    data = load_data()
    email = input("Enter Email: ")
    password = maskpass.askpass(prompt="Enter Password: ",mask="*")
    for user in data["users"]:
        if user["email"] == email and user["password"] == password:
            print(f"Welcome, {user['fname']} {user['lname']}!")  
            return user 
    print("Invalid email or password!")
    return None


def create_project(user):
    data = load_data()
    user_id = user["id"]
    
    print("\nCreating a new project (Enter '0' at any step to return to the main menu)")
    
    while True:
        title = input("Enter your project's title:\n\t").strip()
        if title == "0":
            return
        if title == "":
            print("❌ Project title can't be empty\n")
            continue
        if any(project["title"] == title and project["user_id"] == user_id for project in data["projects"]):
            print("❌ Project already exists! Enter another one\n")
            continue
        break 
    
    while True:
        details = input("Enter your project details:\n\t").strip()
        if details == "0":
            return
        if details == "":
            print("❌ Project details can't be empty\n")
            continue
        else:
            break
    
    while True:
        total_target = input("Enter your project total target:\n\t").strip()
        if total_target == "0":
            return
        try:
            total_target = float(total_target)
            break
        except ValueError:
            print("❌ Invalid total target amount!")
            continue
    
    while True:
        start_date = datetime.datetime.now().date()
        end_date = input(f"Your project campaign starts on {start_date}.\nEnter end date (YYYY-MM-DD):\n\t")
        if end_date == "0":
            return
        try:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date <= start_date:
                print("❌ End date must be after the start date. Please enter a valid future date.")
            else:
                break
        except ValueError:
            print("❌ Invalid date format! Please enter the date in YYYY-MM-DD format.")
    
    data["projects"].append({"user_id":user_id,"title":title,"details": details, "total_target": total_target, "start_date": str(start_date), "end_date": str(end_date)})
    save_data(data)
    print(f"✅ Project {title} added successfully!")


def edit_project(user):
    data = load_data()
    user_id = user["id"]
    user_projects = [p for p in data["projects"] if p["user_id"] == user_id]
    
    if not user_projects:
        print("You have no projects\n")
        return
    
    print("\nEditing a project (Enter '0' at any step to return to the main menu)")
    
    while True:
        print("\nYour Projects:")
        for index, project in enumerate(user_projects, start=1):
            print(f"{index}. {project['title']}")
        
        project_to_edit = input("Enter your project number to edit:\n\t")
        if project_to_edit == "0":
            return
        try:
            project_to_edit = int(project_to_edit)
            if not 1 <= project_to_edit <= len(user_projects):
                print("❌ Invalid project number")
            else:
                break
        except ValueError:
            print("❌ You've entered a non-integer value!")
    
    project = user_projects[project_to_edit - 1]
    
    title = input("Enter your project's title (Press Enter to keep current):\n\t").strip() or project["title"]
    if title == "0":
        return
    details = input("Enter your project details (Press Enter to keep current):\n\t").strip() or project["details"]
    if details == "0":
        return
    
    while True:
        total_target = input("Enter your project total target (Press Enter to keep current):\n\t").strip()
        if total_target == "0":
            return
        if total_target:
            try:
                total_target = float(total_target)
                break
            except ValueError:
                print("❌ Invalid total target amount!")
                continue
        else:
            total_target = project["total_target"]
            break
    
    while True:
        start_date = input("Enter start date (YYYY-MM-DD, Press Enter to keep current):\n\t")
        if start_date == "0":
            return
        if start_date:
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid date format! Please enter the date in YYYY-MM-DD format.")
        else:
            start_date = project["start_date"]
        break
    
    while True:
        end_date = input(f"Your project campaign starts on {start_date}.\nEnter end date (YYYY-MM-DD, Press Enter to keep current):\n\t")
        if end_date == "0":
            return
        if end_date:
            try:
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                if end_date <= start_date:
                    print("❌ End date must be after the start date. Please enter a valid future date.")
                    continue
            except ValueError:
                print("❌ Invalid date format! Please enter the date in YYYY-MM-DD format.")
        else:
            end_date = project["end_date"]
        break
    
    for p in data["projects"]:
        if p["title"] == project["title"] and p["user_id"] == user_id:
            p.update({
                "title": title,
                "details": details,
                "total_target": total_target,
                "start_date": str(start_date),
                "end_date": str(end_date)
            })
            break
    
    save_data(data)
    print(f"✅ Project '{title}' updated successfully!")


def delete_project(user):
    data = load_data()
    user_id = user["id"]
    user_projects = [p for p in data["projects"] if p["user_id"] == user_id]
    
    if not user_projects:
        print("You have no projects\n")
        return
    
    print("\nDeleting a project (Enter '0' to return to the main menu)")
    
    while True:
        print("\nYour Projects:")
        for index, project in enumerate(user_projects, start=1):
            print(f"{index}. {project['title']}")
        
        project_to_delete = input("Enter your project number to delete:\n\t")
        if project_to_delete == "0":
            return
        try:
            project_to_delete = int(project_to_delete)
            if not 1 <= project_to_delete <= len(user_projects):
                print("❌ Invalid project number")
            else:
                break
        except ValueError:
            print("❌ You've entered a non-integer value!")
    
    project = user_projects[project_to_delete - 1]
    
    confirmation = input(f"Are you sure you want to delete '{project['title']}'? (y/n): ")
    if confirmation.lower() != "y":
        print("❌ Deletion cancelled.")
        return
    
    data["projects"] = [p for p in data["projects"] if not (p["title"] == project["title"] and p["user_id"] == user_id)]
    save_data(data)
    print(f"✅ Project '{project['title']}' has been deleted successfully!")



    
def view_projects():
    data = load_data()
    if not data["projects"]:
        print("No projects found!")
        return
    print("\n-" * 40)
    print("\nExisting Projects:\n")
    for project in data["projects"]:
        print(f"Title: {project['title']}")
        print(f"Details: {project['details']}")
        print(f"Total Target: {project['total_target']}")
        print(f"Start Date: {project['start_date']}")
        print(f"End Date: {project['end_date']}")
        print("-" * 40)

def search_project_by_start_date(start_date):
    data = load_data()
    if not data["projects"]:
        print("No projects found!")
        return
    print("-" * 40)
    projects = [p for p in data["projects"] if p["start_date"] == str(start_date)]
    if projects:
        print(f"\nExisting Projects with start date {start_date}:\n")
        for project in projects:
            print(f"Title: {project['title']}")
            print(f"Details: {project['details']}")
            print(f"Total Target: {project['total_target']}")
            print(f"End Date: {project['end_date']}")
            print("-" * 40)
    else:
        print(f"No projects started on {start_date}")

def search_project_by_end_date(end_date):
    data = load_data()
    if not data["projects"]:
        print("No projects found!")
        return
    print("-" * 40)
    projects = [p for p in data["projects"] if p["end_date"] == str(end_date)]
    if projects:
        print(f"\nExisting Projects with end date {end_date}:\n")
        for project in projects:
            print(f"Title: {project['title']}")
            print(f"Details: {project['details']}")
            print(f"Total Target: {project['total_target']}")
            print(f"Start Date: {project['start_date']}")
            print("-" * 40)
    else:
        print(f"No projects will end on {end_date}")



def main():
    while True:
        print("\nCrowd-Funding App\n")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        match choice:
            case "1":
                register()
            case "2":
                user = login()
                if user:
                    while True:
                        print("\n1. Create Project")
                        print("2. View all Projects")
                        print("3. Edit your projects")
                        print("4. Delete a project")
                        print("5. Search by start date")
                        print("6. Search by end date")
                        print("7. Logout")
                        user_choice = input("Choose an option: ")
                        match user_choice:
                            case "1":
                                create_project(user)
                            case "2":
                                view_projects()
                            case "3":
                                edit_project(user)
                            case "4":
                                delete_project(user)
                            case "5":
                                while True:
                                    start_date = input("Enter start date to search by\n\t")
                                    try:
                                        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                                        search_project_by_start_date(start_date)
                                        break
                                    except ValueError:
                                        print("❌ Invalid date format! Please enter the date in YYYY-MM-DD format.")
                            case "6":
                                while True:
                                    end_date = input("Enter end date to search by\n\t")
                                    try:
                                        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                                        search_project_by_end_date(end_date)
                                        break
                                    except ValueError:
                                        print("❌ Invalid date format! Please enter the date in YYYY-MM-DD format.")
                            case "7":
                                break
                            case _:
                                print("❌ Invalid option, try again!")

            case "3":
                print("Goodbye!")
                break
            case _:
                print("❌ Invalid option, try again!")

if __name__ == "__main__":
    main()
