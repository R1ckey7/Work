"""
Currency View Class
Handles currency information display

Author: Rickey
Date: 2025.10.23
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from control.currency_service import CurrencyService


class CurrencyView:
    """View class for handling currency information display"""
    
    def __init__(self):
        """Initialize CurrencyView with console and currency service"""
        self.console = Console()
        self.currency_service = CurrencyService()
    
    def display_exchange_rates(self):
        """Display all exchange rates in a table"""
        self.console.print("\n[bold blue]========== Exchange Rates ==========[/bold blue]\n")
        
        table = Table(title="Exchange Rates (Base: AUD)", box=box.ROUNDED, show_header=True)
        table.add_column("Currency", style="bold cyan", width=20)
        table.add_column("Code", style="bold yellow", width=12)
        table.add_column("Rate to AUD", style="green", justify="right", width=18)
        table.add_column("Rate from AUD", style="magenta", justify="right", width=18)
        
        supported_currencies = self.currency_service.get_supported_currencies()
        
        for currency in supported_currencies:
            try:
                info = self.currency_service.get_rate_info(currency)
                rate_to_aud = info['rate_to_aud']
                rate_from_aud = info['rate_from_aud']
                
                # Format currency name
                currency_names = {
                    'AUD': 'Australian Dollar',
                    'USD': 'US Dollar',
                    'CNY': 'Chinese Yuan',
                    'EUR': 'Euro',
                    'GBP': 'British Pound',
                    'JPY': 'Japanese Yen',
                    'CAD': 'Canadian Dollar',
                    'HKD': 'Hong Kong Dollar'
                }
                
                name = currency_names.get(currency, currency)
                
                # Use bold styling for currency name and code to make them larger/more prominent
                if currency == 'AUD':
                    table.add_row(
                        f"[bold cyan]{name}[/bold cyan]",
                        f"[bold yellow]{currency}[/bold yellow]",
                        "[green]1.0000 (Base)[/green]",
                        "[magenta]1.0000[/magenta]"
                    )
                else:
                    table.add_row(
                        f"[bold cyan]{name}[/bold cyan]",
                        f"[bold yellow]{currency}[/bold yellow]",
                        f"[green]{rate_to_aud:.4f}[/green]",
                        f"[magenta]{rate_from_aud:.4f}[/magenta]"
                    )
                    
            except Exception as e:
                self.console.print(f"[red]Error getting rate for {currency}: {e}[/red]")
        
        self.console.print(table)
        self.console.print(f"\n[dim]Last updated: {self.currency_service.last_updated.strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")
    
    def convert_currency(self):
        """Interactive currency conversion"""
        self.console.print("\n[bold blue]========== Currency Converter ==========[/bold blue]\n")
        
        # Get amount
        while True:
            try:
                amount_str = input("Enter amount to convert: ").strip()
                try:
                    amount = float(amount_str)
                    if amount < 0:
                        self.console.print("[red]Amount cannot be negative![/red]")
                        continue
                    break
                except ValueError:
                    self.console.print("[red]Invalid amount! Please enter a number.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Display currency menu
        currencies = self.currency_service.get_supported_currencies()
        currency_map = {}
        
        table = Table(title="Select Source Currency", box=box.ROUNDED, show_header=True)
        table.add_column("Choice", style="cyan", width=10)
        table.add_column("Currency Code", style="yellow", width=15)
        
        for idx, currency in enumerate(currencies, 1):
            table.add_row(str(idx), currency)
            currency_map[str(idx)] = currency
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print()
        
        # Get source currency
        from_currency = None
        while True:
            try:
                choice = input(f"Select source currency (1-{len(currency_map)}): ").strip()
                if choice in currency_map:
                    from_currency = currency_map[choice]
                    break
                else:
                    self.console.print("[red]Invalid choice! Please select a valid option.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Display target currency menu
        table = Table(title="Select Target Currency", box=box.ROUNDED, show_header=True)
        table.add_column("Choice", style="cyan", width=10)
        table.add_column("Currency Code", style="yellow", width=15)
        
        currency_map.clear()
        for idx, currency in enumerate(currencies, 1):
            table.add_row(str(idx), currency)
            currency_map[str(idx)] = currency
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print()
        
        # Get target currency
        to_currency = None
        while True:
            try:
                choice = input(f"Select target currency (1-{len(currency_map)}): ").strip()
                if choice in currency_map:
                    to_currency = currency_map[choice]
                    break
                else:
                    self.console.print("[red]Invalid choice! Please select a valid option.[/red]")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Cancelled.[/yellow]\n")
                return
        
        # Perform conversion
        try:
            converted = self.currency_service.convert(amount, from_currency, to_currency)
            rate = self.currency_service.get_exchange_rate(from_currency, to_currency)
            
            result_text = f"""
{amount} {from_currency} = {converted} {to_currency}

Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}
            """
            
            self.console.print(Panel(
                result_text.strip(),
                title="Conversion Result",
                border_style="green",
                box=box.ROUNDED
            ))
            self.console.print()
            
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {e}[/bold red]\n")
    
    def display_currency_menu(self):
        """Display currency menu options"""
        menu_text = """
[bold]Currency Menu:[/bold]
[cyan]1.[/cyan] View Exchange Rates
[cyan]2.[/cyan] Currency Converter
[cyan]3.[/cyan] Back to Main Menu
        """
        self.console.print(menu_text)

