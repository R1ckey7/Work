"""
User Service Class
Handles user-related business logic including login verification

Author: Rickey
Date: 2025.10.16
"""

import os
from model.user import User


class UserService:
    """Service class for handling user operations"""
    
    # Reserved usernames that cannot be used
    RESERVED_USERNAMES = ['local', 'default', 'admin', 'root', 'system', 'guest']
    
    def __init__(self, users_file_path: str = "data/users/users.txt"):
        """
        Initialize UserService with users file path
        
        Args:
            users_file_path: Path to the users.txt file
        """
        self.users_file_path = users_file_path
        self.users = {}  # Dictionary to store username: User mappings
    
    def load_users(self) -> bool:
        """
        Load users from the users.txt file
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.users_file_path):
                return False
            
            with open(self.users_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse username:password format
                    if ':' in line:
                        username, password = line.split(':', 1)
                        username = username.strip()
                        password = password.strip()
                        
                        if username:  # Only add if username is not empty
                            user = User(username, password)
                            self.users[username] = user
            
            return True
        except Exception as e:
            print(f"Error loading users: {e}")
            return False
    
    def verify_login(self, username: str, password: str) -> bool:
        """
        Verify user login credentials
        
        Args:
            username: Username to verify
            password: Password to verify
            
        Returns:
            True if credentials are valid, False otherwise
        """
        if not self.users:
            self.load_users()
        
        if username in self.users:
            return self.users[username].password == password
        
        return False
    
    def get_user(self, username: str) -> User:
        """
        Get User object by username
        
        Args:
            username: Username to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        if not self.users:
            self.load_users()
        
        return self.users.get(username)
    
    def user_exists(self, username: str) -> bool:
        """
        Check if a user exists
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists, False otherwise
        """
        if not self.users:
            self.load_users()
        
        return username in self.users
    
    def is_reserved_username(self, username: str) -> bool:
        """
        Check if username is a reserved word
        
        Args:
            username: Username to check
            
        Returns:
            True if username is reserved, False otherwise
        """
        return username.lower() in [reserved.lower() for reserved in self.RESERVED_USERNAMES]
    
    def validate_username(self, username: str) -> tuple:
        """
        Validate username format and availability
        
        Args:
            username: Username to validate
            
        Returns:
            Tuple (is_valid: bool, error_message: str or None)
        """
        if not username:
            return (False, "Username cannot be empty!")
        
        username = username.strip()
        
        # Check if empty after stripping
        if not username:
            return (False, "Username cannot be empty!")
        
        # Check reserved usernames
        if self.is_reserved_username(username):
            return (False, f"Username '{username}' is reserved and cannot be used. Please choose a different username.")
        
        # Check for invalid characters (no dashes, spaces, or special chars that would conflict with folder naming)
        invalid_chars = ['-', ' ', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in username:
                return (False, f"Username cannot contain '{char}'. Please use only letters, numbers, and underscores.")
        
        # Check if username already exists
        if self.user_exists(username):
            return (False, f"Username '{username}' already exists! Please choose a different username.")
        
        return (True, None)
    
    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user
        
        Args:
            username: New username
            password: New password
            
        Returns:
            True if registration successful, False if validation fails or user already exists
        """
        if not self.users:
            self.load_users()
        
        # Validate username before registration
        is_valid, error_message = self.validate_username(username)
        if not is_valid:
            if error_message:
                print(f"Registration failed: {error_message}")
            return False
        
        # Additional check for user existence (redundant but safe)
        if self.user_exists(username):
            print(f"Registration failed: Username '{username}' already exists!")
            return False
        
        try:
            # Append new user to file
            with open(self.users_file_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{username}:{password}")
            
            # Add to memory
            user = User(username, password)
            self.users[username] = user
            
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
