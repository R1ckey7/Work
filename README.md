# Accounting Book - Personal Finance Management System

**USyd COMP9001 Final Project**  
**Author:** Rickey  
**Project Period:** October 15, 2025 - October 30, 2025

<div align="right">
  <a href="README_CN.md">中文版 (Chinese)</a>
</div>

## Project Description

Accounting Book is a practical personal finance management application designed to help users systematically record, categorize, and analyze daily income and expenses, enabling better financial management and fostering good financial habits.

## Core Features

### 1. Multi-Ledger Support
- **Multiple Ledgers**: Users can create and manage multiple ledgers for different purposes (e.g., tourism ledger, living expenses ledger, personal expenses ledger, etc.)
- **Ledger Management**: Create, switch between, view, and manage multiple ledgers
- **Independent Tracking**: Each ledger maintains its own records and statistics independently

### 2. Expense Categorization and Calculation
- **Automatic Categorization**: After users input daily expenses, the system automatically categorizes them into predefined groups (such as food, transportation, entertainment, shopping, medical, etc.)
- **Expense Statistics**: Automatically calculates the total expenditure for each category (per ledger and aggregated)
- **Terminal Display**: Displays expense information by category in table format in the terminal, clear and intuitive

### 3. Statistical Analysis
- **By Year**: View financial statistics by year with currency conversion
- **By Month**: View financial statistics by month with currency conversion
- **Total Summary**: View comprehensive statistics across all ledgers with unified currency display
- **Category Breakdown**: Detailed statistics by income and expense categories

### 4. Transaction Management
- **Add Transactions**: Record income and expenses with date, amount, category, and description
- **Edit Transactions**: Modify existing transaction records
- **Delete Transactions**: Remove transaction records
- **View Transactions**: Browse by year, month, date, or view all

### 5. Currency Support
- **Multi-Currency**: Support for USD, CNY, AUD, EUR, GBP, JPY, CAD, HKD
- **Currency Conversion**: Convert between different currencies using exchange rates
- **Unified Display**: View statistics in selected currency with automatic conversion

## Project Features

- 💻 **Terminal Interface**: Beautiful command-line interface using Rich library
- 🎨 **Interface Beautification**: Colors, tables, panels, and formatted output
- 📝 **File Storage**: CSV/TXT files for data storage, no database required
- 📊 **Statistics**: Comprehensive financial statistics and reporting
- 🔒 **Data Security**: Local file storage, protecting user privacy
- 🔐 **User Authentication**: Login, registration, and guest mode support

## Technology Stack

- **Programming Language**: Python 3.x
- **Data Storage**: CSV/TXT files
  - `users.txt` - User login information
  - `expenses.csv` - Expense records (year, month, day, amount, category, description)
  - `income.csv` - Income records (year, month, day, amount, category, description)
- **Libraries**: 
  - `rich` - Terminal beautification library (required)

## Project Structure

```
Accounting-Book/
├── main.py                    # Main program entry point
├── init_test_data.py          # Initialize test data script
├── model/                     # Model layer (data models)
│   ├── __init__.py
│   ├── user.py               # User model
│   └── ledger.py             # Ledger model
├── visual/                    # View layer (user interface)
│   ├── __init__.py
│   ├── login_view.py         # Login interface
│   ├── register_view.py      # Registration interface
│   ├── ledger_view.py        # Ledger management interface
│   ├── transaction_view.py  # Transaction entry interface
│   ├── currency_view.py      # Currency information interface
│   └── statistics_view.py   # Statistics display interface
├── control/                   # Control layer (business logic)
│   ├── __init__.py
│   ├── user_service.py       # User management service
│   ├── ledger_service.py     # Ledger management service
│   ├── statistics_service.py # Statistics service
│   └── currency_service.py   # Currency conversion service
├── data/                      # Data file directory
│   ├── users/                # User data storage
│   │   ├── users.txt         # User login information
│   │   └── README.md
│   └── ledgers/              # Ledger data storage
│       └── README.md
├── README.md                  # Project documentation (English)
├── README_CN.md              # Project documentation (Chinese)
└── requirements.txt          # Dependencies
```

## Installation

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd Rickey-finalproject

# Install dependencies
pip install rich

# Initialize test data (optional)
python init_test_data.py
```

## Usage Instructions

### Running the Program
```bash
python main.py
```

### Operation Flow
1. **Start Program**: Run `main.py`
2. **Login/Register/Guest**: Choose to login, register, or continue as guest
3. **Main Menu**: 
   - Create new ledger
   - View my ledgers
   - Select ledger
   - Currency information
   - View statistics
   - Logout/Exit
4. **Ledger Menu** (after selecting a ledger):
   - Add expense
   - Add income
   - View expenses (by year/month/date/all)
   - View income (by year/month/date/all)
   - Edit/Delete transactions
5. **Statistics**: View comprehensive financial statistics across all ledgers

### Data File Description
- **users.txt**: Stores usernames and passwords (format: username:password)
- **expenses.csv**: Stores expense records in each ledger folder
- **income.csv**: Stores income records in each ledger folder
- **Folder Structure**: Each ledger is stored in a folder named `{username}-{ledger_name}` or `local-{ledger_name}` for guest mode

## Key Features

1. **Guest Mode**: Use without registration, data stored locally
2. **User Accounts**: Register and login to sync data to cloud (simulated)
3. **Multiple Ledgers**: Create and manage multiple ledgers per user
4. **Currency Support**: Each ledger has its own currency, unchangeable after creation
5. **Statistics**: View statistics by year, month, or total summary with currency conversion
6. **Transaction Management**: Full CRUD operations for transactions

## Testing

To initialize test data for testing:
```bash
python init_test_data.py
```

This will create:
- Test users: zhangsan, lisi, wangwu
- Test ledgers for each user (default, tourism, household)
- Sample expense and income records

## Development Notes

- Project follows MVC (Model-View-Control) architecture
- All dates stored in ISO format (YYYY-MM-DD) internally, displayed as DD/MM/YYYY
- CSV files use format: year, month, day, amount, category, description
- Currency information stored as comment in CSV files

---

**Note**: This project is a course final project aimed at providing a practical personal finance management solution. Uses simple file storage methods, suitable for learning Python basics and file processing.
