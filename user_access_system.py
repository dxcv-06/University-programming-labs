#!/usr/bin/env python3
"""
User Access Management System
System for managing user accounts with different access levels
"""

import hashlib
import datetime
from typing import Optional, Dict, List


class User:
    """Base user class with basic authentication functionality"""
    
    def __init__(self, username: str, password: str, is_active: bool = True):
        """
        Initialize user with username, password hash, and active status
        
        Args:
            username (str): User's username
            password (str): User's plain password (will be hashed)
            is_active (bool): Whether the account is active
        """
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active
    
    def _hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """
        Verify if provided password matches stored password hash
        
        Args:
            password (str): Password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return self.password_hash == self._hash_password(password)
    
    def __str__(self) -> str:
        """String representation of user"""
        status = "Active" if self.is_active else "Inactive"
        return f"{self.__class__.__name__}: {self.username} ({status})"


class Administrator(User):
    """Administrator class with extended permissions"""
    
    def __init__(self, username: str, password: str, permissions: List[str] = None, is_active: bool = True):
        """
        Initialize administrator with additional permissions
        
        Args:
            username (str): Administrator username
            password (str): Administrator password
            permissions (List[str]): List of admin permissions
            is_active (bool): Whether the account is active
        """
        super().__init__(username, password, is_active)
        self.permissions = permissions or [
            "user_management",
            "system_config",
            "database_access",
            "security_settings"
        ]
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if administrator has specific permission
        
        Args:
            permission (str): Permission to check
            
        Returns:
            bool: True if permission exists, False otherwise
        """
        return permission in self.permissions
    
    def add_permission(self, permission: str) -> None:
        """Add new permission to administrator"""
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission: str) -> None:
        """Remove permission from administrator"""
        if permission in self.permissions:
            self.permissions.remove(permission)


class RegularUser(User):
    """Regular user class with basic user functionality"""
    
    def __init__(self, username: str, password: str, is_active: bool = True):
        """
        Initialize regular user
        
        Args:
            username (str): User username
            password (str): User password
            is_active (bool): Whether the account is active
        """
        super().__init__(username, password, is_active)
        self.last_login = None
        self.login_count = 0
    
    def record_login(self) -> None:
        """Record user login timestamp"""
        self.last_login = datetime.datetime.now()
        self.login_count += 1
    
    def get_last_login(self) -> Optional[str]:
        """
        Get formatted last login time
        
        Returns:
            str: Formatted last login time or None if never logged in
        """
        if self.last_login:
            return self.last_login.strftime("%Y-%m-%d %H:%M:%S")
        return None


class GuestUser(User):
    """Guest user class with limited access rights"""
    
    def __init__(self, username: str = "guest", password: str = "guest"):
        """
        Initialize guest user with default credentials and limited access
        
        Args:
            username (str): Guest username (default: "guest")
            password (str): Guest password (default: "guest")
        """
        super().__init__(username, password, is_active=True)
        self.access_level = "read_only"
        self.session_duration = 3600  # 1 hour in seconds
        self.created_at = datetime.datetime.now()
    
    def is_session_expired(self) -> bool:
        """
        Check if guest session has expired
        
        Returns:
            bool: True if session expired, False otherwise
        """
        session_elapsed = (datetime.datetime.now() - self.created_at).total_seconds()
        return session_elapsed > self.session_duration
    
    def get_remaining_time(self) -> int:
        """
        Get remaining session time in seconds
        
        Returns:
            int: Remaining time in seconds
        """
        session_elapsed = (datetime.datetime.now() - self.created_at).total_seconds()
        remaining = max(0, self.session_duration - session_elapsed)
        return int(remaining)


class AccessControl:
    """Access control system for managing users and authentication"""
    
    def __init__(self):
        """Initialize access control system with empty user dictionary"""
        self.users: Dict[str, User] = {}
    
    def add_user(self, user: User) -> bool:
        """
        Add new user to the system
        
        Args:
            user (User): User object to add
            
        Returns:
            bool: True if user added successfully, False if username already exists
        """
        if user.username in self.users:
            print(f"Error: User '{user.username}' already exists!")
            return False
        
        self.users[user.username] = user
        print(f"User '{user.username}' added successfully as {user.__class__.__name__}")
        return True
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password
        
        Args:
            username (str): Username to authenticate
            password (str): Password to verify
            
        Returns:
            User: User object if authentication successful, None otherwise
        """
        # Check if user exists
        if username not in self.users:
            print(f"Authentication failed: User '{username}' not found")
            return None
        
        user = self.users[username]
        
        # Check if account is active
        if not user.is_active:
            print(f"Authentication failed: Account '{username}' is inactive")
            return None
        
        # Check if guest session expired
        if isinstance(user, GuestUser) and user.is_session_expired():
            print(f"Authentication failed: Guest session expired")
            return None
        
        # Verify password
        if not user.verify_password(password):
            print(f"Authentication failed: Invalid password for '{username}'")
            return None
        
        # Record login for regular users
        if isinstance(user, RegularUser):
            user.record_login()
        
        print(f"Authentication successful: Welcome, {username}!")
        return user
    
    def deactivate_user(self, username: str) -> bool:
        """
        Deactivate user account
        
        Args:
            username (str): Username to deactivate
            
        Returns:
            bool: True if deactivated successfully, False otherwise
        """
        if username not in self.users:
            print(f"Error: User '{username}' not found")
            return False
        
        self.users[username].is_active = False
        print(f"User '{username}' has been deactivated")
        return True
    
    def activate_user(self, username: str) -> bool:
        """
        Activate user account
        
        Args:
            username (str): Username to activate
            
        Returns:
            bool: True if activated successfully, False otherwise
        """
        if username not in self.users:
            print(f"Error: User '{username}' not found")
            return False
        
        self.users[username].is_active = True
        print(f"User '{username}' has been activated")
        return True
    
    def list_users(self) -> None:
        """Display all users in the system"""
        if not self.users:
            print("No users in the system")
            return
        
        print("\n" + "="*60)
        print("                    USERS IN SYSTEM")
        print("="*60)
        
        for username, user in self.users.items():
            user_type = user.__class__.__name__
            status = "Active" if user.is_active else "Inactive"
            
            print(f"Username: {username:<15} Type: {user_type:<15} Status: {status}")
            
            # Show additional info based on user type
            if isinstance(user, Administrator):
                print(f"  Permissions: {', '.join(user.permissions)}")
            elif isinstance(user, RegularUser):
                last_login = user.get_last_login()
                login_info = last_login if last_login else "Never"
                print(f"  Last login: {login_info}, Login count: {user.login_count}")
            elif isinstance(user, GuestUser):
                remaining = user.get_remaining_time()
                print(f"  Session remaining: {remaining} seconds")
        
        print("="*60)


def demo_system():
    """Demonstrate the user access management system"""
    print("="*60)
    print("         USER ACCESS MANAGEMENT SYSTEM DEMO")
    print("="*60)
    
    # Create access control system
    access_control = AccessControl()
    
    # Create different types of users
    admin = Administrator("admin", "admin123", ["full_access", "user_management"])
    regular_user = RegularUser("john_doe", "password123")
    guest = GuestUser()
    inactive_user = RegularUser("inactive_user", "pass123", is_active=False)
    
    # Add users to system
    print("\n--- Adding Users ---")
    access_control.add_user(admin)
    access_control.add_user(regular_user)
    access_control.add_user(guest)
    access_control.add_user(inactive_user)
    
    # List all users
    access_control.list_users()
    
    # Test authentication
    print("\n--- Authentication Tests ---")
    
    # Successful authentications
    auth_admin = access_control.authenticate_user("admin", "admin123")
    auth_regular = access_control.authenticate_user("john_doe", "password123")
    auth_guest = access_control.authenticate_user("guest", "guest")
    
    # Failed authentications
    access_control.authenticate_user("admin", "wrongpass")  # Wrong password
    access_control.authenticate_user("nonexistent", "pass")  # User doesn't exist
    access_control.authenticate_user("inactive_user", "pass123")  # Inactive account
    
    # Show user-specific functionality
    if isinstance(auth_admin, Administrator):
        print(f"\nAdmin permissions: {auth_admin.permissions}")
        print(f"Has 'user_management' permission: {auth_admin.has_permission('user_management')}")
    
    if isinstance(auth_regular, RegularUser):
        print(f"\nRegular user last login: {auth_regular.get_last_login()}")
        print(f"Login count: {auth_regular.login_count}")
    
    if isinstance(auth_guest, GuestUser):
        print(f"\nGuest session remaining: {auth_guest.get_remaining_time()} seconds")


if __name__ == "__main__":
    demo_system()
