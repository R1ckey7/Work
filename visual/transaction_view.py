"""
Transaction View Class
Handles transaction (income/expense) entry interface

Author: Rickey
Date: 2025.10.21
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
from control.ledger_service import LedgerService
from control.statistics_service import StatisticsService
from model.ledger import Ledger


class TransactionView:
    """View class for handling transaction entry"""
    
    # Predefined expense categories
    EXPENSE_CATEGORIES = [
        "food",
        "transportation",
        "entertainment",
        "shopping",
        "medical",
        "bills",
        "education",
        "travel",
        "housing",
        "other"
    ]
    
    # Predefined income categories
    INCOME_CATEGORIES = [
        "salary",
        "bonus",
        "investment",
        "gift",
        "refund",
        "freelance",
        "business",
        "rental",
        "other"
    ]
    
    def __init__(self, ledger: Ledger):
        """
        Initialize TransactionView
        
        Args:
            ledger: Current selected ledger
        """
        self.console = Console()
        self.ledger_service = LedgerService()
        self.statistics_service = StatisticsService()
        self.ledger = ledger
    
    def display_ledger_menu(self):
        """Display ledger-specific menu"""
        mode = f"User: {self.ledger.username}" if self.ledger.username else "Guest"
        
        panel_text = f"""
Ledger: {self.ledger.ledger_name}
Currency: {self.ledger.currency}
Mode: {mode}
        """
        
        self.console.print(Panel(panel_text, title="Current Ledger", border_style="cyan"))
        self.console.print("\n[bold]Ledger Menu:[/bold]")
        self.console.print("[cyan]1.[/cyan] Add Expense")
        self.console.print("[cyan]2.[/cyan] Add Income")
        self.console.print("[cyan]3.[/cyan] View Expenses")
        self.console.print("[cyan]4.[/cyan] View Income")
        self.console.print("[cyan]5.[/cyan] Back to Main Menu")
        self.console.print()
    
    def display_category_menu(self, categories: list, title: str) -> dict:
        """
        Display category selection menu
        
        Args:
            categories: List of categories
            title: Menu title
            
        Returns:
            Dictionary mapping choice number to category name
        """
        category_map = {}
        
        table = Table(title=title, box=box.ROUNDED, show_header=True)
        table.add_column("Choice", style="cyan", width=10)
        table.add_column("Category", style="yellow")
        
        for idx, category in enumerate(categories, 1):
            table.add_row(str(idx), category.title())
            category_map[str(idx)] = category
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print()
        
        return category_map
    
    def validate_date(self, date_str: str) -> tuple:
        """
        Validate date format (DD/MM/YYYY) and convert to ISO format (YYYY-MM-DD)
        
        Args:
            date_str: Date string to validate (DD/MM/YYYY format)
            
        Returns:
            Tuple (is_valid: bool, iso_date: str or None)
        """
        try:
            # Parse DD/MM/YYYY format
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            # Convert to ISO format (YYYY-MM-DD) for storage
            iso_date = date_obj.strftime("%Y-%m-%d")
            return (True, iso_date)
        except ValueError:
            try:
                # Also accept YYYY-MM-DD format for backward compatibility
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return (True, date_str)
            except ValueError:
                return (False, None)
    
    def validate_amount(self, amount_str: str) -> float:
        """
        Validate and convert amount
        
        Args:
            amount_str: Amount string to validate
            
        Returns:
            Float amount if valid, None otherwise
        """
        try:
            amount = float(amount_str)
            if amount <= 0:
                return None
            return amount
        except ValueError:
            return None
    
    def get_expense_input(self) -> dict:
        """
        Get expense input from user
        
        Returns:
            Dictionary with expense data or None if cancelled
        """
        self.console.print("\n[bold blue]========== Add Expense ==========[/bold blue]\n")
        
        # Get date - loop until valid
        while True:
            try:
                date_input = input("Enter date (DD/MM/YYYY): ").strip()
                is_valid, date = self.validate_date(date_input)
                if is_valid:
                    break
                else:
                    self.console.print("[red]Invalid date format! Please use DD/MM/YYYY format (e.g., 15/10/2025).[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        # Get amount - loop until valid
        while True:
            try:
                amount_str = input("Enter amount: ").strip()
                amount = self.validate_amount(amount_str)
                if amount is not None:
                    break
                else:
                    self.console.print("[red]Invalid amount! Please enter a positive number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        # Display category menu
        category_map = self.display_category_menu(self.EXPENSE_CATEGORIES, "Select Expense Category")
        
        # Get category choice - loop until valid
        category = None
        while True:
            try:
                choice = input(f"Select category (1-{len(category_map)}): ").strip()
                
                if choice in category_map:
                    category = category_map[choice]
                    break
                else:
                    self.console.print("[red]Invalid category choice! Please select a valid option.[/red]")
                    
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        # Get description (optional)
        try:
            description = input("Enter description (optional, press Enter to skip): ").strip()
        except (EOFError, KeyboardInterrupt):
            description = ""
        
        return {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description,
            'type': 'expense'
        }
    
    def get_income_input(self) -> dict:
        """
        Get income input from user
        
        Returns:
            Dictionary with income data or None if cancelled
        """
        self.console.print("\n[bold blue]========== Add Income ==========[/bold blue]\n")
        
        # Get date - loop until valid
        while True:
            try:
                date_input = input("Enter date (DD/MM/YYYY): ").strip()
                is_valid, date = self.validate_date(date_input)
                if is_valid:
                    break
                else:
                    self.console.print("[red]Invalid date format! Please use DD/MM/YYYY format (e.g., 15/10/2025).[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        # Get amount - loop until valid
        while True:
            try:
                amount_str = input("Enter amount: ").strip()
                amount = self.validate_amount(amount_str)
                if amount is not None:
                    break
                else:
                    self.console.print("[red]Invalid amount! Please enter a positive number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        # Display category menu
        category_map = self.display_category_menu(self.INCOME_CATEGORIES, "Select Income Category")
        
        # Get category choice - loop until valid
        category = None
        while True:
            try:
                choice = input(f"Select category (1-{len(category_map)}): ").strip()
                
                if choice in category_map:
                    category = category_map[choice]
                    break
                else:
                    self.console.print("[red]Invalid category choice! Please select a valid option.[/red]")
                    
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]")
                return None
        
        # Get description (optional)
        try:
            description = input("Enter description (optional, press Enter to skip): ").strip()
        except (EOFError, KeyboardInterrupt):
            description = ""
        
        return {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description,
            'type': 'income'
        }
    
    def add_expense(self) -> bool:
        """
        Add expense transaction
        
        Returns:
            True if added successfully, False otherwise
        """
        transaction_data = self.get_expense_input()
        
        if not transaction_data:
            return False
        
        try:
            success = self.ledger_service.add_expense(
                self.ledger,
                transaction_data['date'],
                transaction_data['amount'],
                transaction_data['category'],
                transaction_data['description']
            )
            
            if success:
                currency = self.ledger.currency
                # Convert ISO date back to DD/MM/YYYY for display
                display_date = datetime.strptime(transaction_data['date'], "%Y-%m-%d").strftime("%d/%m/%Y")
                self.console.print(f"\n[bold green]Expense added successfully![/bold green]")
                self.console.print(f"[dim]{currency} {transaction_data['amount']:.2f} - {transaction_data['category']} on {display_date}[/dim]\n")
            else:
                self.console.print("\n[bold red]Failed to add expense![/bold red]\n")
            
            return success
            
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {e}[/bold red]\n")
            return False
    
    def add_income(self) -> bool:
        """
        Add income transaction
        
        Returns:
            True if added successfully, False otherwise
        """
        transaction_data = self.get_income_input()
        
        if not transaction_data:
            return False
        
        try:
            success = self.ledger_service.add_income(
                self.ledger,
                transaction_data['date'],
                transaction_data['amount'],
                transaction_data['category'],
                transaction_data['description']
            )
            
            if success:
                currency = self.ledger.currency
                # Convert ISO date back to DD/MM/YYYY for display
                display_date = datetime.strptime(transaction_data['date'], "%Y-%m-%d").strftime("%d/%m/%Y")
                self.console.print(f"\n[bold green]Income added successfully![/bold green]")
                self.console.print(f"[dim]{currency} {transaction_data['amount']:.2f} - {transaction_data['category']} on {display_date}[/dim]\n")
            else:
                self.console.print("\n[bold red]Failed to add income![/bold red]\n")
            
            return success
            
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {e}[/bold red]\n")
            return False
    
    def display_expenses_menu(self):
        """Display expenses viewing menu"""
        menu_text = """
[bold]View Expenses Options:[/bold]
[cyan]1.[/cyan] View by Year
[cyan]2.[/cyan] View by Month
[cyan]3.[/cyan] View by Date
[cyan]4.[/cyan] View All Expenses
[cyan]5.[/cyan] Edit/Delete Expense
[cyan]6.[/cyan] Back to Ledger Menu
        """
        self.console.print(menu_text)
    
    def display_expenses(self, show_index: bool = False):
        """Display all expenses in a table
        
        Args:
            show_index: Whether to show index numbers for editing/deleting
        """
        expenses = self.ledger_service.get_expenses(self.ledger)
        
        if not expenses:
            self.console.print("\n[yellow]No expenses found.[/yellow]\n")
            return expenses
        
        table = Table(title=f"All Expenses - {self.ledger.ledger_name}", box=box.ROUNDED, show_header=True)
        if show_index:
            table.add_column("#", style="cyan", width=5)
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Amount", style="red", justify="right", width=15)
        table.add_column("Category", style="yellow", width=15)
        table.add_column("Description", style="white")
        
        currency = self.ledger.currency
        
        for idx, expense in enumerate(expenses):
            # Reconstruct date from year, month, day
            try:
                year = expense.get('year', '')
                month = expense.get('month', '')
                day = expense.get('day', '')
                display_date = f"{day}/{month}/{year}" if all([year, month, day]) else "N/A"
            except:
                display_date = "N/A"
            
            amount_str = f"{currency} {float(expense['amount']):.2f}"
            row_data = []
            if show_index:
                row_data.append(str(idx + 1))
            row_data.extend([
                display_date,
                amount_str,
                expense['category'].title(),
                expense.get('description', '')
            ])
            table.add_row(*row_data)
        
        # Calculate total
        total = sum(float(exp['amount']) for exp in expenses)
        if show_index:
            table.add_row("", "", "", "[bold]Total[/bold]", f"[bold red]{currency} {total:.2f}[/bold red]")
        else:
            table.add_row("", "", "[bold]Total[/bold]", f"[bold red]{currency} {total:.2f}[/bold red]")
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
        
        return expenses
    
    def display_income_menu(self):
        """Display income viewing menu"""
        menu_text = """
[bold]View Income Options:[/bold]
[cyan]1.[/cyan] View by Year
[cyan]2.[/cyan] View by Month
[cyan]3.[/cyan] View by Date
[cyan]4.[/cyan] View All Income
[cyan]5.[/cyan] Edit/Delete Income
[cyan]6.[/cyan] Back to Ledger Menu
        """
        self.console.print(menu_text)
    
    def display_income(self, show_index: bool = False):
        """Display all income in a table
        
        Args:
            show_index: Whether to show index numbers for editing/deleting
        """
        income = self.ledger_service.get_income(self.ledger)
        
        if not income:
            self.console.print("\n[yellow]No income found.[/yellow]\n")
            return income
        
        table = Table(title=f"All Income - {self.ledger.ledger_name}", box=box.ROUNDED, show_header=True)
        if show_index:
            table.add_column("#", style="cyan", width=5)
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Amount", style="green", justify="right", width=15)
        table.add_column("Category", style="yellow", width=15)
        table.add_column("Description", style="white")
        
        currency = self.ledger.currency
        
        for idx, inc in enumerate(income):
            # Reconstruct date from year, month, day
            try:
                year = inc.get('year', '')
                month = inc.get('month', '')
                day = inc.get('day', '')
                display_date = f"{day}/{month}/{year}" if all([year, month, day]) else "N/A"
            except:
                display_date = "N/A"
            
            amount_str = f"{currency} {float(inc['amount']):.2f}"
            row_data = []
            if show_index:
                row_data.append(str(idx + 1))
            row_data.extend([
                display_date,
                amount_str,
                inc['category'].title(),
                inc.get('description', '')
            ])
            table.add_row(*row_data)
        
        # Calculate total
        total = sum(float(inc['amount']) for inc in income)
        if show_index:
            table.add_row("", "", "", "[bold]Total[/bold]", f"[bold green]{currency} {total:.2f}[/bold green]")
        else:
            table.add_row("", "", "[bold]Total[/bold]", f"[bold green]{currency} {total:.2f}[/bold green]")
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
        
        return income
    
    def display_expenses_by_year(self):
        """Display expenses statistics by year"""
        self.console.print("\n[bold blue]========== View Expenses by Year ==========[/bold blue]\n")
        
        # Get year input
        while True:
            try:
                year_str = input("Enter year (YYYY): ").strip()
                year = int(year_str)
                if 1900 <= year <= 2100:
                    break
                else:
                    self.console.print("[red]Please enter a valid year (1900-2100).[/red]")
            except ValueError:
                self.console.print("[red]Invalid year format! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get statistics
        stats = self.statistics_service.get_expenses_by_year(self.ledger, year)
        
        if stats['total'] == 0:
            self.console.print(f"\n[yellow]No expenses found for year {year}.[/yellow]\n")
            return
        
        currency = self.ledger.currency
        
        # Display summary
        summary_text = f"""
Total Expenses: {currency} {stats['total']:.2f}
Year: {year}
        """
        self.console.print(Panel(summary_text.strip(), title="Yearly Summary", border_style="red", box=box.ROUNDED))
        self.console.print()
        
        # Display by category
        if stats['by_category']:
            table = Table(title=f"Expenses by Category - {year}", box=box.ROUNDED, show_header=True)
            table.add_column("Category", style="yellow", width=20)
            table.add_column("Amount", style="red", justify="right", width=18)
            table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / stats['total']) * 100
                table.add_row(
                    category.title(),
                    f"{currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(table)
            self.console.print()
    
    def display_expenses_by_month(self):
        """Display expenses statistics by month"""
        self.console.print("\n[bold blue]========== View Expenses by Month ==========[/bold blue]\n")
        
        # Get year input
        while True:
            try:
                year_str = input("Enter year (YYYY): ").strip()
                year = int(year_str)
                if 1900 <= year <= 2100:
                    break
                else:
                    self.console.print("[red]Please enter a valid year (1900-2100).[/red]")
            except ValueError:
                self.console.print("[red]Invalid year format! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get month input
        while True:
            try:
                month_str = input("Enter month (1-12): ").strip()
                month = int(month_str)
                if 1 <= month <= 12:
                    break
                else:
                    self.console.print("[red]Please enter a valid month (1-12).[/red]")
            except ValueError:
                self.console.print("[red]Invalid month format! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get statistics
        stats = self.statistics_service.get_expenses_by_month(self.ledger, year, month)
        
        if stats['total'] == 0:
            month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            self.console.print(f"\n[yellow]No expenses found for {month_names[month]} {year}.[/yellow]\n")
            return
        
        currency = self.ledger.currency
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        # Display summary
        summary_text = f"""
Total Expenses: {currency} {stats['total']:.2f}
Month: {month_names[month]} {year}
        """
        self.console.print(Panel(summary_text.strip(), title="Monthly Summary", border_style="red", box=box.ROUNDED))
        self.console.print()
        
        # Display by category
        if stats['by_category']:
            table = Table(title=f"Expenses by Category - {month_names[month]} {year}", box=box.ROUNDED, show_header=True)
            table.add_column("Category", style="yellow", width=20)
            table.add_column("Amount", style="red", justify="right", width=18)
            table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / stats['total']) * 100
                table.add_row(
                    category.title(),
                    f"{currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(table)
            self.console.print()
    
    def display_expenses_by_date(self):
        """Display expenses for a specific date"""
        self.console.print("\n[bold blue]========== View Expenses by Date ==========[/bold blue]\n")
        
        # Get date input
        while True:
            try:
                date_input = input("Enter date (DD/MM/YYYY): ").strip()
                is_valid, iso_date = self.validate_date(date_input)
                if is_valid:
                    date_obj = datetime.strptime(iso_date, "%Y-%m-%d")
                    year = date_obj.year
                    month = date_obj.month
                    day = date_obj.day
                    break
                else:
                    self.console.print("[red]Invalid date format! Please use DD/MM/YYYY format (e.g., 15/10/2025).[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get expenses for that date
        expenses = self.statistics_service.get_expenses_by_date(self.ledger, year, month, day)
        
        if not expenses:
            display_date = f"{day}/{month}/{year}"
            self.console.print(f"\n[yellow]No expenses found for {display_date}.[/yellow]\n")
            return
        
        currency = self.ledger.currency
        display_date = f"{day}/{month}/{year}"
        
        table = Table(title=f"Expenses for {display_date}", box=box.ROUNDED, show_header=True)
        table.add_column("Amount", style="red", justify="right", width=18)
        table.add_column("Category", style="yellow", width=20)
        table.add_column("Description", style="white")
        
        total = 0.0
        for expense in expenses:
            amount = float(expense['amount'])
            total += amount
            table.add_row(
                f"{currency} {amount:.2f}",
                expense['category'].title(),
                expense.get('description', '')
            )
        
        table.add_row(f"[bold red]{currency} {total:.2f}[/bold red]", "[bold]Total[/bold]", "")
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print()
    
    def display_income_by_year(self):
        """Display income statistics by year"""
        self.console.print("\n[bold blue]========== View Income by Year ==========[/bold blue]\n")
        
        # Get year input
        while True:
            try:
                year_str = input("Enter year (YYYY): ").strip()
                year = int(year_str)
                if 1900 <= year <= 2100:
                    break
                else:
                    self.console.print("[red]Please enter a valid year (1900-2100).[/red]")
            except ValueError:
                self.console.print("[red]Invalid year format! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get statistics
        stats = self.statistics_service.get_income_by_year(self.ledger, year)
        
        if stats['total'] == 0:
            self.console.print(f"\n[yellow]No income found for year {year}.[/yellow]\n")
            return
        
        currency = self.ledger.currency
        
        # Display summary
        summary_text = f"""
Total Income: {currency} {stats['total']:.2f}
Year: {year}
        """
        self.console.print(Panel(summary_text.strip(), title="Yearly Summary", border_style="green", box=box.ROUNDED))
        self.console.print()
        
        # Display by category
        if stats['by_category']:
            table = Table(title=f"Income by Category - {year}", box=box.ROUNDED, show_header=True)
            table.add_column("Category", style="yellow", width=20)
            table.add_column("Amount", style="green", justify="right", width=18)
            table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / stats['total']) * 100
                table.add_row(
                    category.title(),
                    f"{currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(table)
            self.console.print()
    
    def display_income_by_month(self):
        """Display income statistics by month"""
        self.console.print("\n[bold blue]========== View Income by Month ==========[/bold blue]\n")
        
        # Get year input
        while True:
            try:
                year_str = input("Enter year (YYYY): ").strip()
                year = int(year_str)
                if 1900 <= year <= 2100:
                    break
                else:
                    self.console.print("[red]Please enter a valid year (1900-2100).[/red]")
            except ValueError:
                self.console.print("[red]Invalid year format! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get month input
        while True:
            try:
                month_str = input("Enter month (1-12): ").strip()
                month = int(month_str)
                if 1 <= month <= 12:
                    break
                else:
                    self.console.print("[red]Please enter a valid month (1-12).[/red]")
            except ValueError:
                self.console.print("[red]Invalid month format! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get statistics
        stats = self.statistics_service.get_income_by_month(self.ledger, year, month)
        
        if stats['total'] == 0:
            month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            self.console.print(f"\n[yellow]No income found for {month_names[month]} {year}.[/yellow]\n")
            return
        
        currency = self.ledger.currency
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        # Display summary
        summary_text = f"""
Total Income: {currency} {stats['total']:.2f}
Month: {month_names[month]} {year}
        """
        self.console.print(Panel(summary_text.strip(), title="Monthly Summary", border_style="green", box=box.ROUNDED))
        self.console.print()
        
        # Display by category
        if stats['by_category']:
            table = Table(title=f"Income by Category - {month_names[month]} {year}", box=box.ROUNDED, show_header=True)
            table.add_column("Category", style="yellow", width=20)
            table.add_column("Amount", style="green", justify="right", width=18)
            table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / stats['total']) * 100
                table.add_row(
                    category.title(),
                    f"{currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(table)
            self.console.print()
    
    def display_income_by_date(self):
        """Display income for a specific date"""
        self.console.print("\n[bold blue]========== View Income by Date ==========[/bold blue]\n")
        
        # Get date input
        while True:
            try:
                date_input = input("Enter date (DD/MM/YYYY): ").strip()
                is_valid, iso_date = self.validate_date(date_input)
                if is_valid:
                    date_obj = datetime.strptime(iso_date, "%Y-%m-%d")
                    year = date_obj.year
                    month = date_obj.month
                    day = date_obj.day
                    break
                else:
                    self.console.print("[red]Invalid date format! Please use DD/MM/YYYY format (e.g., 15/10/2025).[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get income for that date
        income = self.statistics_service.get_income_by_date(self.ledger, year, month, day)
        
        if not income:
            display_date = f"{day}/{month}/{year}"
            self.console.print(f"\n[yellow]No income found for {display_date}.[/yellow]\n")
            return
        
        currency = self.ledger.currency
        display_date = f"{day}/{month}/{year}"
        
        table = Table(title=f"Income for {display_date}", box=box.ROUNDED, show_header=True)
        table.add_column("Amount", style="green", justify="right", width=18)
        table.add_column("Category", style="yellow", width=20)
        table.add_column("Description", style="white")
        
        total = 0.0
        for inc in income:
            amount = float(inc['amount'])
            total += amount
            table.add_row(
                f"{currency} {amount:.2f}",
                inc['category'].title(),
                inc.get('description', '')
            )
        
        table.add_row(f"[bold green]{currency} {total:.2f}[/bold green]", "[bold]Total[/bold]", "")
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print()
    
    def edit_delete_expense(self):
        """Edit or delete an expense record"""
        self.console.print("\n[bold blue]========== Edit/Delete Expense ==========[/bold blue]\n")
        
        # Display expenses with indices
        expenses = self.display_expenses(show_index=True)
        
        if not expenses:
            return
        
        # Get record selection
        while True:
            try:
                choice = input(f"\nEnter expense number to edit/delete (1-{len(expenses)}, or 0 to cancel): ").strip()
                if choice == '0':
                    self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                    return
                
                index = int(choice) - 1
                if 0 <= index < len(expenses):
                    break
                else:
                    self.console.print(f"[red]Invalid number! Please enter 1-{len(expenses)} or 0 to cancel.[/red]")
            except ValueError:
                self.console.print("[red]Invalid input! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        selected_expense = expenses[index]
        
        # Display action menu
        self.console.print("\n[bold]Action:[/bold]")
        self.console.print("[cyan]1.[/cyan] Edit")
        self.console.print("[cyan]2.[/cyan] Delete")
        self.console.print("[cyan]3.[/cyan] Cancel")
        
        while True:
            try:
                action = input("\nSelect action (1-3): ").strip()
                if action in ['1', '2', '3']:
                    break
                else:
                    self.console.print("[red]Invalid choice! Please enter 1-3.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        if action == '1':
            # Edit expense
            self.edit_expense(index, selected_expense)
        elif action == '2':
            # Delete expense
            self.delete_expense(index)
    
    def edit_expense(self, index: int, current_expense: dict):
        """Edit an expense record"""
        self.console.print("\n[bold blue]Editing Expense (press Enter to keep current value):[/bold blue]\n")
        
        # Get current values
        try:
            current_date_str = f"{current_expense['day']}/{current_expense['month']}/{current_expense['year']}"
            current_amount = float(current_expense['amount'])
            current_category = current_expense['category']
            current_description = current_expense.get('description', '')
        except:
            self.console.print("[red]Error reading current expense data![/red]")
            return
        
        # Get date
        while True:
            try:
                date_input = input(f"Enter date (DD/MM/YYYY) [{current_date_str}]: ").strip()
                if not date_input:
                    # Use current date
                    date_obj = datetime(int(current_expense['year']), int(current_expense['month']), int(current_expense['day']))
                    iso_date = date_obj.strftime("%Y-%m-%d")
                    break
                
                is_valid, iso_date = self.validate_date(date_input)
                if is_valid:
                    break
                else:
                    self.console.print("[red]Invalid date format! Please use DD/MM/YYYY format.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get amount
        while True:
            try:
                amount_str = input(f"Enter amount [{current_amount:.2f}]: ").strip()
                if not amount_str:
                    amount = current_amount
                    break
                
                amount = self.validate_amount(amount_str)
                if amount is not None:
                    break
                else:
                    self.console.print("[red]Invalid amount! Please enter a positive number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Display category menu
        category_map = self.display_category_menu(self.EXPENSE_CATEGORIES, "Select Expense Category")
        
        # Get category
        while True:
            try:
                choice = input(f"Select category (1-{len(category_map)}) [current: {current_category}]: ").strip()
                if not choice:
                    category = current_category
                    break
                
                if choice in category_map:
                    category = category_map[choice]
                    break
                else:
                    self.console.print("[red]Invalid category choice! Please select a valid option.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get description
        try:
            description = input(f"Enter description [{current_description}]: ").strip()
            if not description:
                description = current_description
        except (EOFError, KeyboardInterrupt):
            description = current_description
        
        # Update expense
        success = self.ledger_service.update_expense(
            self.ledger,
            index,
            iso_date,
            amount,
            category,
            description
        )
        
        if success:
            display_date = datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            self.console.print(f"\n[bold green]Expense updated successfully![/bold green]")
            self.console.print(f"[dim]{self.ledger.currency} {amount:.2f} - {category} on {display_date}[/dim]\n")
        else:
            self.console.print("\n[bold red]Failed to update expense![/bold red]\n")
    
    def delete_expense(self, index: int):
        """Delete an expense record"""
        success = self.ledger_service.delete_expense(self.ledger, index)
        
        if success:
            self.console.print("\n[bold green]Expense deleted successfully![/bold green]\n")
        else:
            self.console.print("\n[bold red]Failed to delete expense![/bold red]\n")
    
    def edit_delete_income(self):
        """Edit or delete an income record"""
        self.console.print("\n[bold blue]========== Edit/Delete Income ==========[/bold blue]\n")
        
        # Display income with indices
        income = self.display_income(show_index=True)
        
        if not income:
            return
        
        # Get record selection
        while True:
            try:
                choice = input(f"\nEnter income number to edit/delete (1-{len(income)}, or 0 to cancel): ").strip()
                if choice == '0':
                    self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                    return
                
                index = int(choice) - 1
                if 0 <= index < len(income):
                    break
                else:
                    self.console.print(f"[red]Invalid number! Please enter 1-{len(income)} or 0 to cancel.[/red]")
            except ValueError:
                self.console.print("[red]Invalid input! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        selected_income = income[index]
        
        # Display action menu
        self.console.print("\n[bold]Action:[/bold]")
        self.console.print("[cyan]1.[/cyan] Edit")
        self.console.print("[cyan]2.[/cyan] Delete")
        self.console.print("[cyan]3.[/cyan] Cancel")
        
        while True:
            try:
                action = input("\nSelect action (1-3): ").strip()
                if action in ['1', '2', '3']:
                    break
                else:
                    self.console.print("[red]Invalid choice! Please enter 1-3.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        if action == '1':
            # Edit income
            self.edit_income(index, selected_income)
        elif action == '2':
            # Delete income
            self.delete_income(index)
    
    def edit_income(self, index: int, current_income: dict):
        """Edit an income record"""
        self.console.print("\n[bold blue]Editing Income (press Enter to keep current value):[/bold blue]\n")
        
        # Get current values
        try:
            current_date_str = f"{current_income['day']}/{current_income['month']}/{current_income['year']}"
            current_amount = float(current_income['amount'])
            current_category = current_income['category']
            current_description = current_income.get('description', '')
        except:
            self.console.print("[red]Error reading current income data![/red]")
            return
        
        # Get date
        while True:
            try:
                date_input = input(f"Enter date (DD/MM/YYYY) [{current_date_str}]: ").strip()
                if not date_input:
                    # Use current date
                    date_obj = datetime(int(current_income['year']), int(current_income['month']), int(current_income['day']))
                    iso_date = date_obj.strftime("%Y-%m-%d")
                    break
                
                is_valid, iso_date = self.validate_date(date_input)
                if is_valid:
                    break
                else:
                    self.console.print("[red]Invalid date format! Please use DD/MM/YYYY format.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get amount
        while True:
            try:
                amount_str = input(f"Enter amount [{current_amount:.2f}]: ").strip()
                if not amount_str:
                    amount = current_amount
                    break
                
                amount = self.validate_amount(amount_str)
                if amount is not None:
                    break
                else:
                    self.console.print("[red]Invalid amount! Please enter a positive number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Display category menu
        category_map = self.display_category_menu(self.INCOME_CATEGORIES, "Select Income Category")
        
        # Get category
        while True:
            try:
                choice = input(f"Select category (1-{len(category_map)}) [current: {current_category}]: ").strip()
                if not choice:
                    category = current_category
                    break
                
                if choice in category_map:
                    category = category_map[choice]
                    break
                else:
                    self.console.print("[red]Invalid category choice! Please select a valid option.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get description
        try:
            description = input(f"Enter description [{current_description}]: ").strip()
            if not description:
                description = current_description
        except (EOFError, KeyboardInterrupt):
            description = current_description
        
        # Update income
        success = self.ledger_service.update_income(
            self.ledger,
            index,
            iso_date,
            amount,
            category,
            description
        )
        
        if success:
            display_date = datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            self.console.print(f"\n[bold green]Income updated successfully![/bold green]")
            self.console.print(f"[dim]{self.ledger.currency} {amount:.2f} - {category} on {display_date}[/dim]\n")
        else:
            self.console.print("\n[bold red]Failed to update income![/bold red]\n")
    
    def delete_income(self, index: int):
        """Delete an income record"""
        success = self.ledger_service.delete_income(self.ledger, index)
        
        if success:
            self.console.print("\n[bold green]Income deleted successfully![/bold green]\n")
        else:
            self.console.print("\n[bold red]Failed to delete income![/bold red]\n")

