"""
User Model Class
Represents a user entity in the system

Author: Rickey
Date: 2025.10.15
"""


class User:
    """User model class for storing user information"""
    
    def __init__(self, username: str, password: str):
        """
        Initialize a User object
        
        Args:
            username: User's username
            password: User's password
        """
        self.username = username
        self.password = password
    
    def __str__(self) -> str:
        """Returns a string representation of the User object"""
        return f"User(username={self.username})"
    
    def __repr__(self) -> str:
        """Returns a representation of the User object"""
        return self.__str__()
