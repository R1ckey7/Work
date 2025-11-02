"""
Login View Class
Handles user login interface and interaction

Author: Rickey
Date: 2025.10.17
"""

from rich.console import Console
from rich.panel import Panel
from rich import box
from control.user_service import UserService
from model.user import User


class LoginView:
    """View class for handling login interface"""
    
    def __init__(self):
        """Initialize LoginView with console and user service"""
        self.console = Console()
        self.user_service = UserService()
        self.current_user: User = None
    
    def display_welcome(self):
        """Display welcome message"""
        welcome_text = """
╔════════════════════════════════════════════╗
║     Accounting Book Management System      ║
║         USyd COMP9001 Final Project        ║
╚════════════════════════════════════════════╝
        """
        self.console.print(welcome_text, style="bold cyan")
        print()
    
    def display_login_menu(self):
        """Display login menu options"""
        menu_text = """
[bold]Please select an option:[/bold]
[cyan]1.[/cyan] Continue as Guest (Local storage only)
[cyan]2.[/cyan] Login (Sync to cloud)
[cyan]3.[/cyan] Register
[cyan]4.[/cyan] Exit
        """
        self.console.print(menu_text)
    
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
    
    def login(self) -> bool:
        """
        Handle user login process with cloud sync simulation
        
        Returns:
            True if login successful, False otherwise
        """
        self.console.print("\n[bold blue]========== Login ==========[/bold blue]\n")
        
        username = self.get_user_input("Enter username")
        if not username:
            self.console.print("[red]Username cannot be empty![/red]")
            return False
        
        password = self.get_user_input("Enter password")
        if not password:
            self.console.print("[red]Password cannot be empty![/red]")
            return False
        
        # Verify login
        if self.user_service.verify_login(username, password):
            self.current_user = self.user_service.get_user(username)
            
            # Ensure default ledger exists for user
            from control.ledger_service import LedgerService
            ledger_service = LedgerService()
            default_ledger = ledger_service.create_default_ledger(username, "AUD")
            
            # Simulate checking for local ledger and syncing to cloud
            import os
            local_ledger_path = "data/ledgers/local_accounts.csv"
            
            if os.path.exists(local_ledger_path):
                self.console.print("\n[bold yellow]Found local ledger data...[/bold yellow]")
                self._simulate_cloud_sync(local_ledger_path, username)
            
            self.console.print(f"\n[bold green]Login successful! Welcome, {username}![/bold green]\n")
            self.console.print("[dim]Your ledger data is now synced to cloud.[/dim]\n")
            return True
        else:
            self.console.print("\n[bold red]Login failed! Invalid username or password.[/bold red]\n")
            return False
    
    def _simulate_cloud_sync(self, local_file: str, username: str):
        """
        Simulate syncing local ledger to cloud
        
        Args:
            local_file: Path to local ledger file
            username: Username for cloud storage
        """
        import time
        import os
        
        # Count records in local file
        record_count = 0
        if os.path.exists(local_file):
            with open(local_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                record_count = len([l for l in lines if l.strip() and not l.startswith('#')]) - 1  # Subtract header
        
        if record_count > 0:
            self.console.print(f"[cyan]Uploading {record_count} records to cloud...[/cyan]")
            
            # Simulate upload progress
            for i in range(3):
                self.console.print(f"[dim]Syncing... [{'.' * (i+1)}][/dim]")
                time.sleep(0.3)
            
            # Move local file to user's cloud storage (simulate)
            user_ledger_path = f"data/ledgers/{username}_accounts.csv"
            self.console.print(f"[green]✓ Successfully synced {record_count} records to cloud[/green]")
            self.console.print(f"[dim]Data stored in: {user_ledger_path}[/dim]")
            
            # In real implementation, you would copy/merge the data
            # For now, we just simulate the process
        else:
            self.console.print("[dim]No local ledger data found.[/dim]")
    
    def continue_as_guest(self) -> bool:
        """
        Continue as guest (local storage only)
        
        Returns:
            True to continue as guest
        """
        # Ensure default ledger exists for guest
        from control.ledger_service import LedgerService
        ledger_service = LedgerService()
        default_ledger = ledger_service.create_default_ledger(None, "AUD")
        
        self.console.print("\n[bold yellow]Continuing as Guest[/bold yellow]")
        self.console.print("[dim]Your data will be stored locally only.[/dim]")
        self.console.print("[dim]Default ledger created automatically.[/dim]")
        self.console.print("[dim]Login later to sync your data to cloud.[/dim]\n")
        self.current_user = None  # No user logged in
        return True
    
    def get_current_user(self) -> User:
        """
        Get currently logged in user
        
        Returns:
            Current User object or None if not logged in
        """
        return self.current_user
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in
        
        Returns:
            True if user is logged in, False otherwise
        """
        return self.current_user is not None

