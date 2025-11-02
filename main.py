"""
Accounting Book - Main Entry Point
USyd COMP9001 Final Project
Author: Rickey
Project Period: October 15, 2025 - October 30, 2025
Main Program Development Date: 2025.10.27
"""

import sys
import io
from visual.login_view import LoginView
from visual.register_view import RegisterView
from visual.ledger_view import LedgerView
from visual.transaction_view import TransactionView
from visual.currency_view import CurrencyView
from visual.statistics_view import StatisticsView

# Set UTF-8 encoding for Windows systems
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def main():
    """Main function to run the Accounting Book application"""
    
    # Initialize views (share the same user_service instance)
    login_view = LoginView()
    register_view = RegisterView(login_view.user_service)
    
    # Load users data
    if not login_view.user_service.load_users():
        print("Error: Failed to load users data!")
        return
    
    # Display welcome message
    login_view.display_welcome()
    
    # Main application loop
    while True:
        # Display login menu
        login_view.display_login_menu()
        
        # Get user choice
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            login_view.console.print("\n[bold yellow]Program interrupted. Goodbye![/bold yellow]\n")
            break
        
        if choice == '1':
            # Continue as guest
            if login_view.continue_as_guest():
                print("\nEntering guest mode...")
                print("Main menu will be implemented here...")
                break  # Exit login loop
                
        elif choice == '2':
            # Login
            if login_view.login():
                # Login successful, user is now logged in
                current_user = login_view.get_current_user()
                print(f"\nLogged in as: {current_user.username}")
                print("Main menu will be implemented here...")
                break  # Exit login loop
                
        elif choice == '3':
            # Register
            if register_view.register():
                # Registration successful, user is now logged in
                current_user = register_view.get_current_user()
                print(f"\nRegistered and logged in as: {current_user.username}")
                print("Main menu will be implemented here...")
                break  # Exit login loop
                
        elif choice == '4':
            # Exit
            login_view.console.print("\n[bold yellow]Thank you for using Accounting Book! Goodbye![/bold yellow]\n")
            return  # Exit the program completely
            
        else:
            login_view.console.print("\n[bold red]Invalid choice! Please enter 1, 2, 3, or 4.[/bold red]\n")
    
    # Only reach here if user successfully logged in, registered, or chose guest mode
    # After login/guest mode, main application menu
    # Get current user from either login_view or register_view
    current_user = None
    if login_view.is_logged_in():
        current_user = login_view.get_current_user()
    elif register_view.is_registered():
        current_user = register_view.get_current_user()
    ledger_view = LedgerView(current_user)
    
    # Initialize default ledger for current user/guest and auto-select it
    from control.ledger_service import LedgerService
    ledger_service = LedgerService()
    
    # Ensure default ledger exists
    default_ledger = ledger_service.create_default_ledger(
        current_user.username if current_user else None,
        "AUD"
    )
    
    if default_ledger:
        ledger_view.set_current_ledger(default_ledger)
    
    if current_user:
        login_view.console.print(f"\n[bold green]Welcome to Accounting Book, {current_user.username}![/bold green]\n")
        if default_ledger:
            login_view.console.print("[dim]Default ledger is ready for use.[/dim]\n")
    else:
        login_view.console.print("\n[bold green]Welcome to Accounting Book! (Guest Mode - Local storage only)[/bold green]\n")
        if default_ledger:
            login_view.console.print("[dim]Default ledger is ready for use.[/dim]\n")
    
    # Initialize currency view
    currency_view = CurrencyView()
    
    # Main application menu
    while True:
        login_view.console.print("[bold]Main Menu:[/bold]")
        login_view.console.print("[cyan]1.[/cyan] Create New Ledger")
        login_view.console.print("[cyan]2.[/cyan] View My Ledgers")
        login_view.console.print("[cyan]3.[/cyan] Select Ledger")
        login_view.console.print("[cyan]4.[/cyan] Currency Information")
        login_view.console.print("[cyan]5.[/cyan] View Statistics")
        login_view.console.print("[cyan]6.[/cyan] Logout/Exit")
        login_view.console.print()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            login_view.console.print("\n[bold yellow]Goodbye![/bold yellow]\n")
            break
        
        if choice == '1':
            # Create new ledger
            ledger = ledger_view.create_new_ledger()
            if ledger:
                ledger_view.set_current_ledger(ledger)
                
        elif choice == '2':
            # View all ledgers
            ledger_view.display_ledgers()
            
        elif choice == '3':
            # Select ledger and enter ledger menu
            ledger = ledger_view.select_ledger()
            if ledger:
                # Enter ledger-specific menu
                transaction_view = TransactionView(ledger)
                
                while True:
                    transaction_view.display_ledger_menu()
                    
                    try:
                        ledger_choice = input("Enter your choice (1-5): ").strip()
                    except (EOFError, KeyboardInterrupt):
                        login_view.console.print("\n[yellow]Returning to main menu...[/yellow]\n")
                        break
                    
                    if ledger_choice == '1':
                        # Add expense
                        transaction_view.add_expense()
                        
                    elif ledger_choice == '2':
                        # Add income
                        transaction_view.add_income()
                        
                    elif ledger_choice == '3':
                        # View expenses - show submenu
                        while True:
                            transaction_view.display_expenses_menu()
                            
                            try:
                                expense_choice = input("Enter your choice (1-6): ").strip()
                            except (EOFError, KeyboardInterrupt):
                                login_view.console.print("\n[yellow]Returning to ledger menu...[/yellow]\n")
                                break
                            
                            if expense_choice == '1':
                                # View by year
                                transaction_view.display_expenses_by_year()
                                
                            elif expense_choice == '2':
                                # View by month
                                transaction_view.display_expenses_by_month()
                                
                            elif expense_choice == '3':
                                # View by date
                                transaction_view.display_expenses_by_date()
                                
                            elif expense_choice == '4':
                                # View all expenses
                                transaction_view.display_expenses()
                                
                            elif expense_choice == '5':
                                # Edit/Delete expense
                                transaction_view.edit_delete_expense()
                                
                            elif expense_choice == '6':
                                # Back to ledger menu
                                break
                                
                            else:
                                login_view.console.print("\n[bold red]Invalid choice! Please enter 1-6.[/bold red]\n")
                        
                    elif ledger_choice == '4':
                        # View income - show submenu
                        while True:
                            transaction_view.display_income_menu()
                            
                            try:
                                income_choice = input("Enter your choice (1-6): ").strip()
                            except (EOFError, KeyboardInterrupt):
                                login_view.console.print("\n[yellow]Returning to ledger menu...[/yellow]\n")
                                break
                            
                            if income_choice == '1':
                                # View by year
                                transaction_view.display_income_by_year()
                                
                            elif income_choice == '2':
                                # View by month
                                transaction_view.display_income_by_month()
                                
                            elif income_choice == '3':
                                # View by date
                                transaction_view.display_income_by_date()
                                
                            elif income_choice == '4':
                                # View all income
                                transaction_view.display_income()
                                
                            elif income_choice == '5':
                                # Edit/Delete income
                                transaction_view.edit_delete_income()
                                
                            elif income_choice == '6':
                                # Back to ledger menu
                                break
                                
                            else:
                                login_view.console.print("\n[bold red]Invalid choice! Please enter 1-6.[/bold red]\n")
                        
                    elif ledger_choice == '5':
                        # Back to main menu
                        break
                        
                    else:
                        login_view.console.print("\n[bold red]Invalid choice! Please enter 1-5.[/bold red]\n")
                
                # Update ledger_view with selected ledger
                ledger_view.set_current_ledger(ledger)
            
        elif choice == '4':
            # Currency Information
            while True:
                currency_view.display_currency_menu()
                
                try:
                    currency_choice = input("Enter your choice (1-3): ").strip()
                except (EOFError, KeyboardInterrupt):
                    login_view.console.print("\n[yellow]Returning to main menu...[/yellow]\n")
                    break
                
                if currency_choice == '1':
                    # View exchange rates
                    currency_view.display_exchange_rates()
                    
                elif currency_choice == '2':
                    # Currency converter
                    currency_view.convert_currency()
                    
                elif currency_choice == '3':
                    # Back to main menu
                    break
                    
                else:
                    login_view.console.print("\n[bold red]Invalid choice! Please enter 1-3.[/bold red]\n")
                
        elif choice == '5':
            # View statistics
            username = current_user.username if current_user else None
            statistics_view = StatisticsView(username)
            
            while True:
                statistics_view.display_statistics_menu()
                
                try:
                    stats_choice = input("Enter your choice (1-4): ").strip()
                except (EOFError, KeyboardInterrupt):
                    login_view.console.print("\n[yellow]Returning to main menu...[/yellow]\n")
                    break
                
                if stats_choice == '1':
                    # Select by year
                    statistics_view.display_statistics_by_year()
                    
                elif stats_choice == '2':
                    # Select by month
                    statistics_view.display_statistics_by_month()
                    
                elif stats_choice == '3':
                    # Total summary
                    statistics_view.display_total_summary()
                    
                elif stats_choice == '4':
                    # Back to main menu
                    break
                    
                else:
                    login_view.console.print("\n[bold red]Invalid choice! Please enter 1-4.[/bold red]\n")
                
        elif choice == '6':
            # Logout/Exit
            login_view.console.print("\n[bold yellow]Thank you for using Accounting Book! Goodbye![/bold yellow]\n")
            break
            
        else:
            login_view.console.print("\n[bold red]Invalid choice! Please enter 1-6.[/bold red]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

