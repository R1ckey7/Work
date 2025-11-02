"""
Statistics View Class
Handles main menu statistics display

Author: Rickey
Date: 2025.10.25
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
from control.statistics_service import StatisticsService
from control.ledger_service import LedgerService
from control.currency_service import CurrencyService
from model.ledger import Ledger


class StatisticsView:
    """View class for handling main menu statistics"""
    
    def __init__(self, username: str = None):
        """
        Initialize StatisticsView
        
        Args:
            username: Current user's username, None for guest
        """
        self.console = Console()
        self.statistics_service = StatisticsService()
        self.ledger_service = LedgerService()
        self.currency_service = CurrencyService()
        self.username = username
    
    def display_statistics_menu(self):
        """Display statistics menu"""
        menu_text = """
[bold]Statistics Menu:[/bold]
[cyan]1.[/cyan] Select by Year
[cyan]2.[/cyan] Select by Month
[cyan]3.[/cyan] Total Summary
[cyan]4.[/cyan] Back to Main Menu
        """
        self.console.print(menu_text)
    
    def display_statistics_by_year(self):
        """Display statistics for a specific year across all ledgers"""
        self.console.print("\n[bold blue]========== Statistics by Year ==========[/bold blue]\n")
        
        # Get currency selection
        supported_currencies = self.currency_service.get_supported_currencies()
        
        self.console.print("[bold]Select display currency:[/bold]")
        currency_map = {}
        for idx, curr in enumerate(supported_currencies, 1):
            currency_map[str(idx)] = curr
            self.console.print(f"[cyan]{idx}.[/cyan] {curr}")
        
        while True:
            try:
                choice = input(f"\nSelect currency (1-{len(supported_currencies)}): ").strip()
                if choice in currency_map:
                    target_currency = currency_map[choice]
                    break
                else:
                    self.console.print(f"[red]Invalid choice! Please enter 1-{len(supported_currencies)}.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
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
        
        # Get all ledgers for the user
        ledgers = self.ledger_service.list_user_ledgers(self.username)
        
        if not ledgers:
            self.console.print("\n[yellow]No ledgers found.[/yellow]\n")
            return
        
        # Calculate totals across all ledgers (convert to target currency)
        total_income = 0.0
        total_expenses = 0.0
        income_by_category = {}
        expenses_by_category = {}
        
        # Store converted amounts for each ledger
        ledger_summaries = []
        
        for ledger in ledgers:
            # Get year statistics for this ledger
            income_stats = self.statistics_service.get_income_by_year(ledger, year)
            expense_stats = self.statistics_service.get_expenses_by_year(ledger, year)
            
            ledger_income = income_stats['total']
            ledger_expenses = expense_stats['total']
            
            # Convert to target currency
            converted_income = self.currency_service.convert(ledger_income, ledger.currency, target_currency)
            converted_expenses = self.currency_service.convert(ledger_expenses, ledger.currency, target_currency)
            
            total_income += converted_income
            total_expenses += converted_expenses
            
            # Store for display
            ledger_summaries.append({
                'ledger': ledger,
                'income': converted_income,
                'expenses': converted_expenses,
                'balance': converted_income - converted_expenses
            })
            
            # Aggregate by category (convert to target currency)
            for category, amount in income_stats['by_category'].items():
                converted_amount = self.currency_service.convert(amount, ledger.currency, target_currency)
                if category in income_by_category:
                    income_by_category[category] += converted_amount
                else:
                    income_by_category[category] = converted_amount
            
            for category, amount in expense_stats['by_category'].items():
                converted_amount = self.currency_service.convert(amount, ledger.currency, target_currency)
                if category in expenses_by_category:
                    expenses_by_category[category] += converted_amount
                else:
                    expenses_by_category[category] = converted_amount
        
        total_income = round(total_income, 2)
        total_expenses = round(total_expenses, 2)
        total_balance = round(total_income - total_expenses, 2)
        
        # Round category totals
        for category in income_by_category:
            income_by_category[category] = round(income_by_category[category], 2)
        for category in expenses_by_category:
            expenses_by_category[category] = round(expenses_by_category[category], 2)
        
        # Display total summary
        summary_text = f"""
Total Income: {target_currency} {total_income:.2f}
Total Expenses: {target_currency} {total_expenses:.2f}
Total Balance (Surplus): {target_currency} {total_balance:.2f}
Year: {year}
        """
        balance_color = "green" if total_balance >= 0 else "red"
        panel = Panel(summary_text.strip(), title="Yearly Financial Summary", border_style=balance_color, box=box.ROUNDED)
        self.console.print(panel)
        self.console.print()
        
        # Display summary by ledger
        self.console.print(f"\n[bold]Year {year} Summary by Ledger ({target_currency}):[/bold]\n")
        summary_table = Table(title=f"Financial Summary by Ledger - {year}", box=box.ROUNDED, show_header=True)
        summary_table.add_column("Ledger", style="cyan", width=20)
        summary_table.add_column("Original Currency", style="yellow", width=15)
        summary_table.add_column("Total Income", style="green", justify="right", width=18)
        summary_table.add_column("Total Expenses", style="red", justify="right", width=18)
        summary_table.add_column("Balance", style="magenta", justify="right", width=18)
        
        for summary in ledger_summaries:
            ledger = summary['ledger']
            income = summary['income']
            expenses = summary['expenses']
            balance = summary['balance']
            
            balance_color = "green" if balance >= 0 else "red"
            summary_table.add_row(
                ledger.ledger_name,
                ledger.currency,
                f"{target_currency} {income:.2f}",
                f"{target_currency} {expenses:.2f}",
                f"[{balance_color}]{target_currency} {balance:.2f}[/{balance_color}]"
            )
        
        self.console.print(summary_table)
        self.console.print()
        
        # Display income by category
        if income_by_category:
            income_cat_table = Table(title=f"Income by Category - {year} ({target_currency})", box=box.ROUNDED, show_header=True)
            income_cat_table.add_column("Category", style="yellow", width=20)
            income_cat_table.add_column("Total Amount", style="green", justify="right", width=18)
            income_cat_table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(income_by_category.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / total_income * 100) if total_income > 0 else 0
                income_cat_table.add_row(
                    category.title(),
                    f"{target_currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(income_cat_table)
            self.console.print()
        
        # Display expenses by category
        if expenses_by_category:
            expense_cat_table = Table(title=f"Expenses by Category - {year} ({target_currency})", box=box.ROUNDED, show_header=True)
            expense_cat_table.add_column("Category", style="yellow", width=20)
            expense_cat_table.add_column("Total Amount", style="red", justify="right", width=18)
            expense_cat_table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                expense_cat_table.add_row(
                    category.title(),
                    f"{target_currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(expense_cat_table)
            self.console.print()
    
    def display_statistics_by_month(self):
        """Display statistics for a specific month across all ledgers"""
        self.console.print("\n[bold blue]========== Statistics by Month ==========[/bold blue]\n")
        
        # Get currency selection
        supported_currencies = self.currency_service.get_supported_currencies()
        
        self.console.print("[bold]Select display currency:[/bold]")
        currency_map = {}
        for idx, curr in enumerate(supported_currencies, 1):
            currency_map[str(idx)] = curr
            self.console.print(f"[cyan]{idx}.[/cyan] {curr}")
        
        while True:
            try:
                choice = input(f"\nSelect currency (1-{len(supported_currencies)}): ").strip()
                if choice in currency_map:
                    target_currency = currency_map[choice]
                    break
                else:
                    self.console.print(f"[red]Invalid choice! Please enter 1-{len(supported_currencies)}.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
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
        
        # Get all ledgers for the user
        ledgers = self.ledger_service.list_user_ledgers(self.username)
        
        if not ledgers:
            self.console.print("\n[yellow]No ledgers found.[/yellow]\n")
            return
        
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        month_name = month_names[month]
        
        # Calculate totals across all ledgers (convert to target currency)
        total_income = 0.0
        total_expenses = 0.0
        income_by_category = {}
        expenses_by_category = {}
        
        # Store converted amounts for each ledger
        ledger_summaries = []
        
        for ledger in ledgers:
            # Get month statistics for this ledger
            income_stats = self.statistics_service.get_income_by_month(ledger, year, month)
            expense_stats = self.statistics_service.get_expenses_by_month(ledger, year, month)
            
            ledger_income = income_stats['total']
            ledger_expenses = expense_stats['total']
            
            # Convert to target currency
            converted_income = self.currency_service.convert(ledger_income, ledger.currency, target_currency)
            converted_expenses = self.currency_service.convert(ledger_expenses, ledger.currency, target_currency)
            
            total_income += converted_income
            total_expenses += converted_expenses
            
            # Store for display
            ledger_summaries.append({
                'ledger': ledger,
                'income': converted_income,
                'expenses': converted_expenses,
                'balance': converted_income - converted_expenses
            })
            
            # Aggregate by category (convert to target currency)
            for category, amount in income_stats['by_category'].items():
                converted_amount = self.currency_service.convert(amount, ledger.currency, target_currency)
                if category in income_by_category:
                    income_by_category[category] += converted_amount
                else:
                    income_by_category[category] = converted_amount
            
            for category, amount in expense_stats['by_category'].items():
                converted_amount = self.currency_service.convert(amount, ledger.currency, target_currency)
                if category in expenses_by_category:
                    expenses_by_category[category] += converted_amount
                else:
                    expenses_by_category[category] = converted_amount
        
        total_income = round(total_income, 2)
        total_expenses = round(total_expenses, 2)
        total_balance = round(total_income - total_expenses, 2)
        
        # Round category totals
        for category in income_by_category:
            income_by_category[category] = round(income_by_category[category], 2)
        for category in expenses_by_category:
            expenses_by_category[category] = round(expenses_by_category[category], 2)
        
        # Display total summary
        summary_text = f"""
Total Income: {target_currency} {total_income:.2f}
Total Expenses: {target_currency} {total_expenses:.2f}
Total Balance (Surplus): {target_currency} {total_balance:.2f}
Month: {month_name} {year}
        """
        balance_color = "green" if total_balance >= 0 else "red"
        panel = Panel(summary_text.strip(), title="Monthly Financial Summary", border_style=balance_color, box=box.ROUNDED)
        self.console.print(panel)
        self.console.print()
        
        # Display summary by ledger
        self.console.print(f"\n[bold]{month_name} {year} Summary by Ledger ({target_currency}):[/bold]\n")
        summary_table = Table(title=f"Financial Summary by Ledger - {month_name} {year}", box=box.ROUNDED, show_header=True)
        summary_table.add_column("Ledger", style="cyan", width=20)
        summary_table.add_column("Original Currency", style="yellow", width=15)
        summary_table.add_column("Total Income", style="green", justify="right", width=18)
        summary_table.add_column("Total Expenses", style="red", justify="right", width=18)
        summary_table.add_column("Balance", style="magenta", justify="right", width=18)
        
        for summary in ledger_summaries:
            ledger = summary['ledger']
            income = summary['income']
            expenses = summary['expenses']
            balance = summary['balance']
            
            balance_color = "green" if balance >= 0 else "red"
            summary_table.add_row(
                ledger.ledger_name,
                ledger.currency,
                f"{target_currency} {income:.2f}",
                f"{target_currency} {expenses:.2f}",
                f"[{balance_color}]{target_currency} {balance:.2f}[/{balance_color}]"
            )
        
        self.console.print(summary_table)
        self.console.print()
        
        # Display income by category
        if income_by_category:
            income_cat_table = Table(title=f"Income by Category - {month_name} {year} ({target_currency})", box=box.ROUNDED, show_header=True)
            income_cat_table.add_column("Category", style="yellow", width=20)
            income_cat_table.add_column("Total Amount", style="green", justify="right", width=18)
            income_cat_table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(income_by_category.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / total_income * 100) if total_income > 0 else 0
                income_cat_table.add_row(
                    category.title(),
                    f"{target_currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(income_cat_table)
            self.console.print()
        
        # Display expenses by category
        if expenses_by_category:
            expense_cat_table = Table(title=f"Expenses by Category - {month_name} {year} ({target_currency})", box=box.ROUNDED, show_header=True)
            expense_cat_table.add_column("Category", style="yellow", width=20)
            expense_cat_table.add_column("Total Amount", style="red", justify="right", width=18)
            expense_cat_table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                expense_cat_table.add_row(
                    category.title(),
                    f"{target_currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(expense_cat_table)
            self.console.print()
    
    def display_total_summary(self):
        """Display total summary across all ledgers with currency conversion"""
        self.console.print("\n[bold blue]========== Total Summary ==========[/bold blue]\n")
        
        # Get currency selection
        supported_currencies = self.currency_service.get_supported_currencies()
        
        self.console.print("[bold]Select display currency:[/bold]")
        currency_map = {}
        for idx, curr in enumerate(supported_currencies, 1):
            currency_map[str(idx)] = curr
            self.console.print(f"[cyan]{idx}.[/cyan] {curr}")
        
        while True:
            try:
                choice = input(f"\nSelect currency (1-{len(supported_currencies)}): ").strip()
                if choice in currency_map:
                    target_currency = currency_map[choice]
                    break
                else:
                    self.console.print(f"[red]Invalid choice! Please enter 1-{len(supported_currencies)}.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Get all ledgers for the user
        ledgers = self.ledger_service.list_user_ledgers(self.username)
        
        if not ledgers:
            self.console.print("\n[yellow]No ledgers found.[/yellow]\n")
            return
        
        # Calculate totals across all ledgers (convert to target currency)
        total_income = 0.0
        total_expenses = 0.0
        expenses_by_category = {}
        
        for ledger in ledgers:
            # Get all expenses and income
            expenses = self.ledger_service.get_expenses(ledger)
            income = self.ledger_service.get_income(ledger)
            
            # Convert and sum expenses
            for expense in expenses:
                try:
                    amount = float(expense['amount'])
                    # Convert to target currency
                    converted_amount = self.currency_service.convert(amount, ledger.currency, target_currency)
                    total_expenses += converted_amount
                    
                    # Aggregate by category
                    category = expense['category']
                    if category in expenses_by_category:
                        expenses_by_category[category] += converted_amount
                    else:
                        expenses_by_category[category] = converted_amount
                except (ValueError, KeyError):
                    continue
            
            # Convert and sum income
            for inc in income:
                try:
                    amount = float(inc['amount'])
                    # Convert to target currency
                    converted_amount = self.currency_service.convert(amount, ledger.currency, target_currency)
                    total_income += converted_amount
                except (ValueError, KeyError):
                    continue
        
        total_income = round(total_income, 2)
        total_expenses = round(total_expenses, 2)
        balance = round(total_income - total_expenses, 2)
        
        # Round category totals
        for category in expenses_by_category:
            expenses_by_category[category] = round(expenses_by_category[category], 2)
        
        # Display total summary
        summary_text = f"""
Total Income: {target_currency} {total_income:.2f}
Total Expenses: {target_currency} {total_expenses:.2f}
Balance (Surplus): {target_currency} {balance:.2f}
        """
        balance_color = "green" if balance >= 0 else "red"
        panel = Panel(summary_text.strip(), title="Total Financial Summary", border_style=balance_color, box=box.ROUNDED)
        self.console.print(panel)
        self.console.print()
        
        # Display expenses by category
        if expenses_by_category:
            expense_cat_table = Table(title=f"Total Expenses by Category ({target_currency})", box=box.ROUNDED, show_header=True)
            expense_cat_table.add_column("Category", style="yellow", width=20)
            expense_cat_table.add_column("Total Amount", style="red", justify="right", width=18)
            expense_cat_table.add_column("Percentage", style="cyan", justify="right", width=12)
            
            # Sort by amount descending
            sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                expense_cat_table.add_row(
                    category.title(),
                    f"{target_currency} {amount:.2f}",
                    f"{percentage:.1f}%"
                )
            
            self.console.print(expense_cat_table)
            self.console.print()

