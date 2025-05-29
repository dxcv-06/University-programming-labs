#!/usr/bin/env python3
"""
User Manager Class for SQLite Database Operations
This module contains the UserManager class for handling user operations
"""

import sqlite3
import hashlib
import os

class UserManager:
    def __init__(self, db_name="users_database.db"):
        """
        Initialize the UserManager with database connection
        
        Args:
            db_name (str): Name of the database file
        """
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """
        Create database and users table if they don't exist
        This function is safe to call multiple times - won't cause errors
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Create users table with required columns
            # IF NOT EXISTS prevents errors if table already exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Check if this is a new database
            if not os.path.exists(self.db_name) or os.path.getsize(self.db_name) == 0:
                print(f"New database '{self.db_name}' created successfully.")
            else:
                print(f"Connected to existing database '{self.db_name}'.")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def hash_password(self, password):
        """
        Hash password using SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def add_user(self, login, password, full_name):
        """
        Add a new user to the database
        
        Args:
            login (str): User login name
            password (str): User password (will be hashed)
            full_name (str): User's full name
            
        Returns:
            bool: True if user added successfully, False otherwise
        """
        if not all([login, password, full_name]):
            print("Error: All fields (login, password, full_name) are required!")
            return False
            
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Hash the password before storing
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (login, password, full_name)
                VALUES (?, ?, ?)
            ''', (login.strip(), hashed_password, full_name.strip()))
            
            conn.commit()
            conn.close()
            print(f"User '{login}' added successfully!")
            return True
            
        except sqlite3.IntegrityError:
            print(f"Error: User with login '{login}' already exists!")
            return False
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_password(self, login, new_password):
        """
        Update user's password
        
        Args:
            login (str): User login name
            new_password (str): New password (will be hashed)
            
        Returns:
            bool: True if password updated successfully, False otherwise
        """
        if not login or not new_password:
            print("Error: Login and new password are required!")
            return False
            
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE login = ?', (login.strip(),))
            if not cursor.fetchone():
                print(f"Error: User '{login}' not found!")
                conn.close()
                return False
            
            # Hash new password and update
            hashed_password = self.hash_password(new_password)
            cursor.execute('''
                UPDATE users SET password = ? WHERE login = ?
            ''', (hashed_password, login.strip()))
            
            conn.commit()
            conn.close()
            print(f"Password updated successfully for user '{login}'!")
            return True
            
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
    
    def authenticate_user(self, login, password):
        """
        Authenticate user by checking login and password
        
        Args:
            login (str): User login name
            password (str): User password
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not login or not password:
            print("Error: Login and password are required!")
            return False
            
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get user's hashed password from database
            cursor.execute('SELECT password, full_name FROM users WHERE login = ?', (login.strip(),))
            result = cursor.fetchone()
            
            if not result:
                print(f"Authentication failed: User '{login}' not found!")
                conn.close()
                return False
            
            stored_password, full_name = result
            hashed_input_password = self.hash_password(password)
            
            conn.close()
            
            # Compare hashed passwords
            if stored_password == hashed_input_password:
                print(f"Authentication successful! Welcome, {full_name}!")
                return True
            else:
                print("Authentication failed: Incorrect password!")
                return False
                
        except Exception as e:
            print(f"Error during authentication: {e}")
            return False
    
    def list_users(self):
        """Display all users (for administrative purposes)"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT login, full_name, created_at FROM users ORDER BY created_at')
            users = cursor.fetchall()
            
            if users:
                print("\n" + "="*60)
                print("                 REGISTERED USERS")
                print("="*60)
                print(f"{'Login':<15} {'Full Name':<25} {'Created At':<20}")
                print("-"*60)
                for login, full_name, created_at in users:
                    print(f"{login:<15} {full_name:<25} {created_at:<20}")
                print("-"*60)
                print(f"Total users: {len(users)}")
            else:
                print("No users found in database.")
            
            conn.close()
            
        except Exception as e:
            print(f"Error listing users: {e}")
    
    def user_exists(self, login):
        """
        Check if user exists in database
        
        Args:
            login (str): User login name
            
        Returns:
            bool: True if user exists, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM users WHERE login = ?', (login.strip(),))
            result = cursor.fetchone()
            
            conn.close()
            return result is not None
            
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
    
    def get_user_count(self):
        """
        Get total number of users in database
        
        Returns:
            int: Number of users
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
            
        except Exception as e:
            print(f"Error getting user count: {e}")
            return 0
