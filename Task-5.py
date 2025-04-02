import hashlib
import getpass
import time

def hash_password(password):
    """
    Function to hash a password using MD5
    """
    return hashlib.md5(password.encode()).hexdigest()

def verify_password(username, password, users_dict):
    """
    Function checks the correctness of the entered password for a user
    """
    if username in users_dict:
        hashed_password = hash_password(password)
        return hashed_password == users_dict[username]["password"]
    return False

def create_user(username, password, full_name, users_dict):
    """
    Function to create a new user
    """
    if username in users_dict:
        return False, "Username already exists"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if not full_name or len(full_name.strip()) < 3:
        return False, "Full name must be at least 3 characters long"
    
    # Create new user with hashed password
    users_dict[username] = {
        "password": hash_password(password),
        "full_name": full_name
    }
    
    return True, "User created successfully"

def delete_user(username, users_dict):
    """
    Function to delete a user
    """
    if username in users_dict:
        del users_dict[username]
        return True, f"User '{username}' deleted successfully"
    return False, f"User '{username}' not found"

def change_password(target_username, new_password, users_dict):
    """
    Function to change a user's password (admin function)
    """
    if target_username not in users_dict:
        return False, "User not found"
    
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long"
    
    users_dict[target_username]["password"] = hash_password(new_password)
    return True, f"Password for {target_username} changed successfully"

def change_own_password(username, old_password, new_password, users_dict):
    """
    Function for a user to change their own password
    """
    if username not in users_dict:
        return False, "User not found"
    
    if not verify_password(username, old_password, users_dict):
        return False, "Current password is incorrect"
    
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long"
    
    users_dict[username]["password"] = hash_password(new_password)
    return True, "Password changed successfully"

def display_users(users_dict, show_passwords=False):
    """
    Display all users in a formatted table
    If show_passwords is True, also display hashed passwords (admin only)
    """
    if not users_dict:
        print("\nNo users in the system.")
        return
    
    print("\n" + "=" * 80)
    print("User List")
    print("=" * 80)
    
    if show_passwords:
        print(f"{'Username':<15} | {'Full Name':<30} | {'Hashed Password':<32}")
        print("-" * 80)
        
        for username, data in users_dict.items():
            print(f"{username:<15} | {data['full_name']:<30} | {data['password']:<32}")
    else:
        print(f"{'Username':<15} | {'Full Name':<30}")
        print("-" * 50)
        
        for username, data in users_dict.items():
            print(f"{username:<15} | {data['full_name']:<30}")
    
    print("-" * (80 if show_passwords else 50))
    print(f"Total: {len(users_dict)} user(s)")

def login_attempt(users_dict):
    """
    Function for user login with limited attempts
    """
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        print("\nLogin")
        username = input("Username: ")
        password = getpass.getpass("Password: ")  # Hide password input
        
        if verify_password(username, password, users_dict):
            print(f"\nLogin successful! Welcome, {users_dict[username]['full_name']}!")
            return username
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Invalid username or password. {remaining} attempt(s) remaining.")
            else:
                print("Too many failed attempts. Please try again later.")
                time.sleep(2)  # Add a short delay after failed attempts
                return None
    
    return None

def is_admin(username):
    """
    Check if the user is an administrator
    """
    return username == "admin"

def interactive_user_management():
    """
    Interactive UI for user management system with role-based access control
    """
    # Initialize with sample users
    users = {
        "admin": {
            "password": hash_password("admin123"),
            "full_name": "System Administrator"
        },
        "user1": {
            "password": hash_password("password123"),
            "full_name": "John Smith"
        }
    }
    
    current_user = None
    
    print("\nWelcome to User Management System")
    
    while True:
        if current_user:
            # User is logged in
            is_admin_user = is_admin(current_user)
            
            print(f"\nLogged in as: {current_user} ({users[current_user]['full_name']})")
            print("Role: " + ("Administrator" if is_admin_user else "Regular User"))
            
            print("\nUser Management System")
            print("1. View User List")
            print("2. Change My Password")
            
            # Admin-only options
            if is_admin_user:
                print("3. Create New User")
                print("4. Delete User")
                print("5. Change User Password")
                print("6. View Hashed Passwords")
                print("7. Logout")
                print("8. Exit System")
            else:
                # Regular user options
                print("3. Logout")
                print("4. Exit System")
            
            # Get user choice
            max_choice = 8 if is_admin_user else 4
            choice = input(f"\nEnter your choice (1-{max_choice}): ")
            
            # Process common options
            if choice == "1":
                # View user list (without passwords for regular users)
                display_users(users, show_passwords=False)
                
            elif choice == "2":
                # Change own password
                print("\nChange My Password")
                old_password = getpass.getpass("Current Password: ")
                new_password = getpass.getpass("New Password: ")
                confirm_password = getpass.getpass("Confirm New Password: ")
                
                if new_password != confirm_password:
                    print("Error: Passwords do not match.")
                    continue
                
                success, message = change_own_password(current_user, old_password, new_password, users)
                print(message)
            
            # Admin-specific options
            elif choice == "3" and is_admin_user:
                # Create new user (admin only)
                print("\nCreate New User")
                new_username = input("Username: ")
                
                # Basic validation
                if not new_username or " " in new_username:
                    print("Error: Username cannot be empty or contain spaces.")
                    continue
                
                new_password = getpass.getpass("Password: ")
                confirm_password = getpass.getpass("Confirm Password: ")
                
                if new_password != confirm_password:
                    print("Error: Passwords do not match.")
                    continue
                
                full_name = input("Full Name: ")
                
                success, message = create_user(new_username, new_password, full_name, users)
                print(message)
                
            elif choice == "4" and is_admin_user:
                # Delete user (admin only)
                if len(users) <= 1:
                    print("Error: Cannot delete the last user in the system.")
                    continue
                
                print("\nDelete User")
                display_users(users)
                
                username_to_delete = input("\nEnter username to delete (or 0 to cancel): ")
                
                if username_to_delete == "0":
                    continue
                
                if username_to_delete == "admin":
                    print("Error: Cannot delete the admin account.")
                    continue
                
                confirm = input(f"Are you sure you want to delete user '{username_to_delete}'? (y/n): ")
                
                if confirm.lower() == "y":
                    success, message = delete_user(username_to_delete, users)
                    print(message)
                else:
                    print("Deletion cancelled.")
                    
            elif choice == "5" and is_admin_user:
                # Change user password (admin only)
                print("\nChange User Password")
                display_users(users)
                
                target_user = input("\nEnter username to change password (or 0 to cancel): ")
                
                if target_user == "0":
                    continue
                
                if target_user not in users:
                    print(f"Error: User '{target_user}' not found.")
                    continue
                
                new_password = getpass.getpass("New Password: ")
                confirm_password = getpass.getpass("Confirm New Password: ")
                
                if new_password != confirm_password:
                    print("Error: Passwords do not match.")
                    continue
                
                success, message = change_password(target_user, new_password, users)
                print(message)
                
            elif choice == "6" and is_admin_user:
                # View hashed passwords (admin only)
                print("\nViewing Hashed Passwords (Admin Only)")
                display_users(users, show_passwords=True)
            
            # Logout option (different number for admin/regular)
            elif (choice == "7" and is_admin_user) or (choice == "3" and not is_admin_user):
                print(f"Logging out user: {current_user}")
                current_user = None
                time.sleep(1)
                
            # Exit option (different number for admin/regular)
            elif (choice == "8" and is_admin_user) or (choice == "4" and not is_admin_user):
                print("Exiting User Management System. Goodbye!")
                break
                
            else:
                print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")
                
        else:
            # Not logged in yet
            print("\nUser Management System")
            print("1. Login")
            print("2. Exit")
            
            choice = input("\nEnter your choice (1-2): ")
            
            if choice == "1":
                # Login
                current_user = login_attempt(users)
            
            elif choice == "2":
                # Exit
                print("Exiting User Management System. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    # Run the user management system
    interactive_user_management()
    
    # For demonstration and testing:
    print("\nTest Users:")
    print("Username: admin, Password: admin123")
    print("Username: user1, Password: password123")
