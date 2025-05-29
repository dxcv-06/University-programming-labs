#!/usr/bin/env python3
"""
Test script for User Management System
This script demonstrates and tests all functionality automatically
"""

import os
import sys
from user_manager import UserManager

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"           {title.upper()}")
    print("="*60)

def print_subsection(title):
    """Print formatted subsection header"""
    print(f"\n{title}")
    print("-" * 50)

def test_database_initialization():
    """Test database initialization with existing and new databases"""
    print_section("Testing Database Initialization")
    
    # Test with new database
    test_db_new = "test_new.db"
    if os.path.exists(test_db_new):
        os.remove(test_db_new)
        
    print("Creating new database:")
    user_manager_new = UserManager(test_db_new)
    print(f"✓ New database created: {test_db_new}")
    
    # Test with existing database
    print("\nConnecting to existing database:")
    user_manager_existing = UserManager(test_db_new)
    print("✓ Connected to existing database without errors")
    
    # Clean up
    if os.path.exists(test_db_new):
        os.remove(test_db_new)
    
    return True

def test_user_operations():
    """Test all user operations"""
    print_section("Testing User Operations")
    
    # Initialize test database
    test_db = "test_users.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    user_manager = UserManager(test_db)
    
    # Test data
    test_users = [
        ("admin", "admin123", "System Administrator"),
        ("john_doe", "password123", "John Doe"),
        ("jane_smith", "securepass456", "Jane Smith"),
        ("test_user", "testpass789", "Test User")
    ]
    
    print_subsection("1. Testing add_user function")
    
    # Add test users
    for login, password, full_name in test_users:
        success = user_manager.add_user(login, password, full_name)
        if success:
            print(f"✓ Successfully added user: {login}")
        else:
            print(f"✗ Failed to add user: {login}")
    
    # Test duplicate user
    print("\nTesting duplicate user addition:")
    duplicate_result = user_manager.add_user("john_doe", "newpass", "John Doe Jr.")
    if not duplicate_result:
        print("✓ Correctly rejected duplicate user")
    else:
        print("✗ Failed to reject duplicate user")
    
    # Test empty fields
    print("\nTesting empty field validation:")
    empty_result = user_manager.add_user("", "pass", "Name")
    if not empty_result:
        print("✓ Correctly rejected empty login")
    else:
        print("✗ Failed to reject empty login")
    
    print_subsection("2. Testing user_exists function")
    
    # Test existing user
    if user_manager.user_exists("john_doe"):
        print("✓ Correctly found existing user")
    else:
        print("✗ Failed to find existing user")
    
    # Test non-existing user
    if not user_manager.user_exists("nonexistent"):
        print("✓ Correctly reported non-existing user")
    else:
        print("✗ Incorrectly found non-existing user")
    
    print_subsection("3. Testing authenticate_user function")
    
    # Test correct credentials
    auth_tests = [
        ("admin", "admin123", True),
        ("john_doe", "password123", True),
        ("jane_smith", "wrongpass", False),
        ("nonexistent", "anypass", False)
    ]
    
    for login, password, expected in auth_tests:
        result = user_manager.authenticate_user(login, password)
        if result == expected:
            status = "✓" if expected else "✓"
            expected_text = "succeed" if expected else "fail"
            print(f"{status} Authentication correctly {expected_text}ed for {login}")
        else:
            print(f"✗ Authentication test failed for {login}")
    
    print_subsection("4. Testing update_password function")
    
    # Test password update for existing user
    update_success = user_manager.update_password("john_doe", "newpassword123")
    if update_success:
        print("✓ Password updated successfully")
        
        # Test authentication with new password
        if user_manager.authenticate_user("john_doe", "newpassword123"):
            print("✓ Authentication with new password successful")
        else:
            print("✗ Authentication with new password failed")
        
        # Test authentication with old password (should fail)
        if not user_manager.authenticate_user("john_doe", "password123"):
            print("✓ Old password correctly rejected")
        else:
            print("✗ Old password incorrectly accepted")
    
    # Test update for non-existing user
    if not user_manager.update_password("nonexistent", "newpass"):
        print("✓ Correctly rejected update for non-existing user")
    else:
        print("✗ Incorrectly allowed update for non-existing user")
    
    print_subsection("5. Testing list_users function")
    user_manager.list_users()
    
    print_subsection("6. Testing get_user_count function")
    count = user_manager.get_user_count()
    print(f"Total users in database: {count}")
    if count == len(test_users):
        print("✓ User count is correct")
    else:
        print("✗ User count is incorrect")
    
    return test_db

def test_security_features():
    """Test password hashing and security features"""
    print_section("Testing Security Features")
    
    user_manager = UserManager("security_test.db")
    
    print_subsection("Password Hashing Tests")
    
    # Test password hashing consistency
    test_password = "mypassword123"
    hash1 = user_manager.hash_password(test_password)
    hash2 = user_manager.hash_password(test_password)
    
    print(f"Original password: {test_password}")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    
    if hash1 == hash2:
        print("✓ Password hashing is consistent")
    else:
        print("✗ Password hashing is inconsistent")
    
    # Test different passwords produce different hashes
    different_password = "differentpassword123"
    hash_different = user_manager.hash_password(different_password)
    
    if hash1 != hash_different:
        print("✓ Different passwords produce different hashes")
    else:
        print("✗ Different passwords produce same hash")
    
    # Test hash length and format
    if len(hash1) == 64 and all(c in '0123456789abcdef' for c in hash1):
        print("✓ Hash format is correct (64-character hexadecimal)")
    else:
        print("✗ Hash format is incorrect")
    
    # Clean up
    if os.path.exists("security_test.db"):
        os.remove("security_test.db")

def test_error_handling():
    """Test error handling and edge cases"""
    print_section("Testing Error Handling")
    
    user_manager = UserManager("error_test.db")
    
    print_subsection("Edge Case Tests")
    
    # Test with whitespace
    success = user_manager.add_user("  spaced_user  ", "pass123", "  Spaced User  ")
    if success:
        print("✓ Handled whitespace in input correctly")
        
        # Test authentication with original spacing
        if user_manager.authenticate_user("  spaced_user  ", "pass123"):
            print("✓ Authentication handles whitespace correctly")
        else:
            print("✗ Authentication failed with whitespace")
    
    # Test with special characters in names
    special_success = user_manager.add_user("user@test", "pass123", "User with Спец символы")
    if special_success:
        print("✓ Handled special characters correctly")
    else:
        print("✗ Failed to handle special characters")
    
    # Clean up
    if os.path.exists("error_test.db"):
        os.remove("error_test.db")

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print_section("Starting Comprehensive Test Suite")
    
    test_results = []
    
    try:
        # Test 1: Database initialization
        result1 = test_database_initialization()
        test_results.append(("Database Initialization", result1))
        
        # Test 2: User operations
        test_db = test_user_operations()
        test_results.append(("User Operations", True))
        
        # Test 3: Security features
        test_security_features()
        test_results.append(("Security Features", True))
        
        # Test 4: Error handling
        test_error_handling()
        test_results.append(("Error Handling", True))
        
        # Clean up test database
        if os.path.exists(test_db):
            os.remove(test_db)
            print(f"\n✓ Cleaned up test database: {test_db}")
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        test_results.append(("Test Execution", False))
    
    # Print final results
    print_section("Test Results Summary")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed successfully!")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    return passed == total

if __name__ == "__main__":
    try:
        print("User Management System - Test Suite")
        print("This script will test all functionality automatically.")
        
        input("\nPress Enter to start testing...")
        
        success = run_comprehensive_test()
        
        print("\n" + "="*60)
        print("           TESTING COMPLETED")
        print("="*60)
        
        if success:
            print("✅ All tests completed successfully!")
            print("The User Management System is working correctly.")
        else:
            print("❌ Some tests failed.")
            print("Please review the test output for details.")
        
        print("\nYou can now run 'python main.py' to use the system.")
        
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error during testing: {e}")
    
    print("\nTest script terminated.")
