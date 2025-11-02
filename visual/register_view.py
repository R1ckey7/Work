"""
Register View Class
Handles user registration interface and interaction

Author: Rickey
Date: 2025.10.26
"""

from rich.console import Console
from control.user_service import UserService
from control.ledger_service import LedgerService
from model.user import User


class RegisterView:
    """View class for handling user registration"""
    
    def __init__(self, user_service: UserService = None):
        """
        Initialize RegisterView with console and user service
        
        Args:
            user_service: Optional UserService instance (if None, creates new one)
        """
        self.console = Console()
        self.user_service = user_service if user_service else UserService()
        self.ledger_service = LedgerService()
        self.current_user: User = None
    
    def get_user_input(self, prompt: str) -> str:
        """
        Get user input with prompt
        
        Args:
            prompt: Prompt message to display
            
        Returns:
            User input string
        """
        try:
            return input(f"{prompt}: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise
    
    def register(self) -> bool:
        """
        Handle user registration process with automatic default ledger creation
        
        Returns:
            True if registration successful, False otherwise
        """
        self.console.print("\n[bold blue]========== Register ==========[/bold blue]\n")
        
        # Get username - loop until valid
        username = None
        while True:
            try:
                username = self.get_user_input("Enter new username")
                is_valid, error_message = self.user_service.validate_username(username)
                
                if is_valid:
                    break
                else:
                    self.console.print(f"[red]{error_message}[/red]")
                    
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return False
        
        # Get password - loop until valid
        password = None
        while True:
            try:
                password = self.get_user_input("Enter password")
                if not password:
                    self.console.print("[red]Password cannot be empty! Please enter a password.[/red]")
                else:
                    break
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return False
        
        # Confirm password - loop until valid
        while True:
            try:
                confirm_password = self.get_user_input("Confirm password")
                if password == confirm_password:
                    break
                else:
                    self.console.print("[red]Passwords do not match! Please try again.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return False
        
        # Register user
        if self.user_service.register_user(username, password):
            self.current_user = self.user_service.get_user(username)
            
            # Create default ledger for new user (with AUD currency)
            try:
                default_ledger = self.ledger_service.create_default_ledger(username, "AUD")
                if default_ledger:
                    self.console.print("\n[bold green]Registration successful! Welcome, {}![/bold green]".format(username))
                    self.console.print("[dim]Default ledger created automatically.[/dim]")
                    self.console.print("[dim]Your ledger data is now synced to cloud.[/dim]\n")
                else:
                    self.console.print("\n[bold green]Registration successful! Welcome, {}![/bold green]".format(username))
                    self.console.print("[yellow]Note: Default ledger creation failed. You can create one manually.[/yellow]\n")
            except Exception as e:
                self.console.print("\n[bold green]Registration successful! Welcome, {}![/bold green]".format(username))
                self.console.print("[yellow]Note: Error creating default ledger: {}[/yellow]\n".format(e))
            
            return True
        else:
            self.console.print("\n[bold red]Registration failed![/bold red]\n")
            return False
    
    def get_current_user(self) -> User:
        """
        Get currently registered/logged in user
        
        Returns:
            Current User object or None if not registered
        """
        return self.current_user
    
    def is_registered(self) -> bool:
        """
        Check if user is registered
        
        Returns:
            True if user is registered, False otherwise
        """
        return self.current_user is not None

