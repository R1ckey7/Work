"""
Ledger View Class
Handles ledger creation interface and interaction

Author: Rickey
Date: 2025.10.20
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from control.ledger_service import LedgerService
from model.ledger import Ledger
from model.user import User


class LedgerView:
    """View class for handling ledger interface"""
    
    def __init__(self, current_user: User = None):
        """
        Initialize LedgerView
        
        Args:
            current_user: Current logged in user, None for guest mode
        """
        self.console = Console()
        self.ledger_service = LedgerService()
        self.current_user = current_user
        self.current_ledger: Ledger = None
    
    def display_currency_menu(self) -> dict:
        """
        Display currency selection menu
        
        Returns:
            Dictionary mapping choice number to currency code
        """
        currencies = LedgerService.SUPPORTED_CURRENCIES
        currency_map = {}
        
        table = Table(title="Select Currency", box=box.ROUNDED, show_header=True)
        table.add_column("Choice", style="cyan", width=10)
        table.add_column("Currency Code", style="yellow", width=15)
        table.add_column("Currency Name", style="green")
        
        choice_num = 1
        for code, name in currencies.items():
            table.add_row(str(choice_num), code, name)
            currency_map[str(choice_num)] = code
            choice_num += 1
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n[dim]Note: Currency cannot be changed after ledger creation![/dim]\n")
        
        return currency_map
    
    def create_new_ledger(self) -> Ledger:
        """
        Handle new ledger creation process
        
        Returns:
            Ledger object if created successfully, None otherwise
        """
        self.console.print("\n[bold blue]========== Create New Ledger ==========[/bold blue]\n")
        
        # Get ledger name - loop until valid
        ledger_name = None
        while True:
            try:
                ledger_name = input("Enter ledger name: ").strip()
                if ledger_name:
                    username = self.current_user.username if self.current_user else None
                    if not self.ledger_service.ledger_exists(ledger_name, username):
                        break
                    else:
                        mode = f"for user '{username}'" if username else "in guest mode"
                        self.console.print(f"[red]Ledger '{ledger_name}' already exists {mode}! Please choose a different name.[/red]")
                else:
                    self.console.print("[red]Ledger name cannot be empty! Please enter a name.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        username = self.current_user.username if self.current_user else None
        
        # Display currency selection
        currency_map = self.display_currency_menu()
        
        # Get currency choice - loop until valid
        currency = None
        while True:
            try:
                choice = input(f"\nSelect currency (1-{len(currency_map)}): ").strip()
                
                if choice in currency_map:
                    currency = currency_map[choice]
                    break
                else:
                    self.console.print("[red]Invalid choice! Please select a valid option.[/red]")
                    
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        # Create ledger
        try:
            self.console.print("\n[cyan]Creating ledger...[/cyan]")
            
            ledger = self.ledger_service.create_ledger(ledger_name, currency, username)
            
            self.console.print(f"\n[bold green]Ledger '{ledger_name}' created successfully![/bold green]")
            self.console.print(f"[dim]Folder: {ledger.get_folder_path()}[/dim]")
            self.console.print(f"[dim]Currency: {currency}[/dim]")
            
            self.current_ledger = ledger
            return ledger
            
        except Exception as e:
            self.console.print(f"\n[bold red]Failed to create ledger: {e}[/bold red]")
            return None
    
    def list_ledgers(self) -> list:
        """
        List all ledgers for current user/guest
        
        Returns:
            List of Ledger objects
        """
        username = self.current_user.username if self.current_user else None
        ledgers = self.ledger_service.list_user_ledgers(username)
        return ledgers
    
    def display_ledgers(self):
        """Display all ledgers in a table"""
        ledgers = self.list_ledgers()
        
        if not ledgers:
            mode = "logged in" if self.current_user else "guest mode"
            self.console.print("\n[yellow]No ledgers found. Create a new ledger to get started![/yellow]\n")
            return
        
        table = Table(title="Your Ledgers", box=box.ROUNDED, show_header=True)
        table.add_column("#", style="cyan", width=5)
        table.add_column("Ledger Name", style="yellow")
        table.add_column("Currency", style="green", width=10)
        table.add_column("Mode", style="magenta", width=10)
        
        for idx, ledger in enumerate(ledgers, 1):
            mode = f"User" if ledger.username else "Guest"
            table.add_row(str(idx), ledger.ledger_name, ledger.currency, mode)
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
    
    def select_ledger(self) -> Ledger:
        """
        Allow user to select a ledger from list
        
        Returns:
            Selected Ledger object or None
        """
        ledgers = self.list_ledgers()
        
        if not ledgers:
            self.console.print("\n[yellow]No ledgers available. Please create a ledger first.[/yellow]\n")
            return None
        
        self.display_ledgers()
        
        while True:
            try:
                choice = input(f"Select ledger (1-{len(ledgers)}): ").strip()
                idx = int(choice) - 1
                
                if 0 <= idx < len(ledgers):
                    selected_ledger = ledgers[idx]
                    self.current_ledger = selected_ledger
                    self.console.print(f"\n[green]Selected ledger: {selected_ledger.ledger_name}[/green]\n")
                    return selected_ledger
                else:
                    self.console.print("[red]Invalid choice! Please select a number between 1 and {}.[/red]".format(len(ledgers)))
                    
            except ValueError:
                self.console.print("[red]Invalid input! Please enter a valid number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
    
    def get_current_ledger(self) -> Ledger:
        """Get currently selected ledger"""
        return self.current_ledger
    
    def set_current_ledger(self, ledger: Ledger):
        """Set current ledger"""
        self.current_ledger = ledger

