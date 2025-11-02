"""
Ledger Model Class
Represents a ledger/account book entity

Author: Rickey
Date: 2025.10.18
"""


class Ledger:
    """Ledger model class for storing ledger information"""
    
    def __init__(self, ledger_name: str, currency: str, username: str = None):
        """
        Initialize a Ledger object
        
        Args:
            ledger_name: Name of the ledger
            currency: Currency code (e.g., USD, CNY, AUD) - cannot be changed after creation
            username: Username if logged in, None for guest mode
        """
        self.ledger_name = ledger_name
        self.currency = currency
        self.username = username  # None for guest mode
        self._folder_path = self._generate_folder_path()
    
    def _generate_folder_path(self) -> str:
        """
        Generate folder path for this ledger
        
        Returns:
            Folder path string
        """
        if self.username:
            # Logged in user: username-ledger_name
            return f"data/ledgers/{self.username}-{self.ledger_name}"
        else:
            # Guest mode: local-ledger_name
            return f"data/ledgers/local-{self.ledger_name}"
    
    def get_folder_path(self) -> str:
        """Get the folder path for this ledger"""
        return self._folder_path
    
    def get_expenses_file_path(self) -> str:
        """Get the expenses CSV file path"""
        return f"{self._folder_path}/expenses.csv"
    
    def get_income_file_path(self) -> str:
        """Get the income CSV file path"""
        return f"{self._folder_path}/income.csv"
    
    def __str__(self) -> str:
        """Returns a string representation of the Ledger object"""
        mode = f"User: {self.username}" if self.username else "Guest"
        return f"Ledger(name={self.ledger_name}, currency={self.currency}, {mode})"
    
    def __repr__(self) -> str:
        """Returns a representation of the Ledger object"""
        return self.__str__()
