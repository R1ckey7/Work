# Ledger Data Storage Directory

This directory is used to store ledger record files.

## Multi-Ledger Support
**Important**: A single user can have multiple ledgers (e.g., tourism ledger, living expenses ledger, etc.)

## File Description
- `local_accounts_{ledger_name}.csv` - Guest mode ledger files (local storage only)
- `{username}_accounts_{ledger_name}.csv` - User ledger files (synced to cloud)
  - Example: `zhangsan_accounts_tourism.csv`, `zhangsan_accounts_living.csv`
- `{username}_settings.txt` - User settings (spending limits, savings goals, ledger list, etc.)

## File Format
CSV format: `date,type,category,amount,notes`
- date: Transaction date (stored as YYYY-MM-DD in CSV, displayed as DD/MM/YYYY in UI)
- type: income or expense
- category: food, transportation, entertainment, shopping, medical, etc.
- amount: Transaction amount (decimal)
- notes: Additional notes/description
