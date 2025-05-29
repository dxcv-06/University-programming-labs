#!/usr/bin/env python3
"""
Main program for User Management System
This file contains the main menu and user interface
"""

import getpass
import sys
from user_manager import UserManager

def display_header():
    """Display program header"""
    print("\n" + "="*60)
    print("           USER MANAGEMENT SYSTEM v1.0")
    print("="*60)

def display_menu():
    """Display main menu options"""
    print("\nChoose an option:")
    print("1. Add new user")
    print("2. Update user password")
    print("3. Authenticate user")
    print("4. List all users")
    print("5. Show database statistics")
    print("6. Exit")
    print("-"*60)

def get_user_input(prompt, password=False, required=True):
    """
    Get user input with validation
    
    Args:
        prompt (str): Input prompt message
        password (bool): Whether to hide input (for passwords)
        required (bool): Whether input is required
        
    Returns:
        str: User input or None if not required and empty
    """
    while True:
        if password:
            value = getpass.getpass(prompt)
        else:
            value = input(prompt).strip()
        
        if value or not required:
            return value
        
        print("This field is required! Please enter a value.")

def add_new_user(user_manager):
    """Handle adding new user"""
    print("\n" + "="*40)
    print("           ADD NEW USER")
    print("="*40)
    
    login = get_user_input("Enter login: ")
    
    # Check if user already exists
    if user_manager.user_exists(login):
        print(f"Error: User '{login}' already exists!")
        return
    
    password = get_user_input("Enter password: ", password=True)
    confirm_password = get_user_input("Confirm password: ", password=True)
    
    if password != confirm_password:
        print("Error: Passwords do not match!")
        return
    
    full_name = get_user_input("Enter full name: ")
    
    # Confirm user creation
    print(f"\nConfirm user creation:")
    print(f"Login: {login}")
    print(f"Full Name: {full_name}")
    
    confirm = input("Create this user? (y/n): ").lower().strip()
    if confirm == 'y' or confirm == 'yes':
        user_manager.add_user(login, password, full_name)
    else:
        print("User creation cancelled.")

def update_user_password(user_manager):
    """Handle updating user password"""
    print("\n" + "="*40)
    print("          UPDATE PASSWORD")
    print("="*40)
    
    login = get_user_input("Enter login: ")
    
    # Check if user exists
    if not user_manager.user_exists(login):
        print(f"Error: User '{login}' not found!")
        return
    
    # Authenticate current user first
    current_password = get_user_input("Enter current password: ", password=True)
    if not user_manager.authenticate_user(login, current_password):
        print("Cannot update password: Current password is incorrect!")
        return
    
    new_password = get_user_input("Enter new password: ", password=True)
    confirm_password = get_user_input("Confirm new password: ", password=True)
    
    if new_password != confirm_password:
        print("Error: New passwords do not match!")
        return
    
    user_manager.update_password(login, new_password)

def authenticate_user(user_manager):
    """Handle user authentication"""
    print("\n" + "="*40)
    print("        USER AUTHENTICATION")
    print("="*40)
    
    login = get_user_input("Enter login: ")
    password = get_user_input("Enter password: ", password=True)
    
    success = user_manager.authenticate_user(login, password)
    
    if success:
        print("✓ Authentication successful!")
    else:
        print("✗ Authentication failed!")
    
    return success

def show_statistics(user_manager):
    """Show database statistics"""
    print("\n" + "="*40)
    print("       DATABASE STATISTICS")
    print("="*40)
    
    user_count = user_manager.get_user_count()
    print(f"Total registered users: {user_count}")
    
    if user_count > 0:
        print("\nWould you like to see the user list? (y/n): ", end="")
        show_list = input().lower().strip()
        if show_list == 'y' or show_list == 'yes':
            user_manager.list_users()

def main():
    """Main program function"""
    try:
        # Initialize user manager
        display_header()
        print("Initializing database...")
        user_manager = UserManager()
        
        # Show initial statistics
        user_count = user_manager.get_user_count()
        if user_count > 0:
            print(f"Found {user_count} existing users in database.")
        else:
            print("Database is empty. You can start by adding users.")
        
        # Main program loop
        while True:
            display_menu()
            
            try:
                choice = input("Enter your choice (1-6): ").strip()
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                break
            
            if choice == '1':
                add_new_user(user_manager)
            
            elif choice == '2':
                update_user_password(user_manager)
            
            elif choice == '3':
                authenticate_user(user_manager)
            
            elif choice == '4':
                user_manager.list_users()
            
            elif choice == '5':
                show_statistics(user_manager)
            
            elif choice == '6':
                print("\nThank you for using User Management System!")
                print("Goodbye! 👋")
                break
            
            else:
                print("❌ Invalid choice! Please enter a number between 1-6.")
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please restart the program.")
    finally:
        print("Program terminated.")

if __name__ == "__main__":
    main()
