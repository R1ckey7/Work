# Design Notes - Accounting Book System

## Important Design Requirements

### Multi-Ledger Support
**Key Requirement**: A single user can have multiple ledgers/account books.

#### Examples:
- Tourism ledger (for travel expenses)
- Living expenses ledger (for food and accommodation)
- Personal expenses ledger
- Business expenses ledger
- etc.

#### Implementation Considerations:
1. **Data Structure**: Need to support ledger name/category identification
2. **File Storage**: 
   - Guest mode: `local_accounts_{ledger_name}.csv`
   - Logged in users: `{username}_{ledger_name}_accounts.csv`
3. **User Interface**: Allow users to:
   - Create new ledgers
   - Switch between ledgers
   - View all their ledgers
   - Delete/rename ledgers
4. **Data Model**: 
   - Each ledger entry should include a `ledger_name` or `ledger_id` field
   - User settings should track multiple ledgers per user

### Authentication & Storage Strategy
- **Guest Mode**: Data stored locally only in `data/ledgers/local_*.csv`
- **Logged In**: Data synced to cloud (simulated) in `data/ledgers/{username}_*.csv`
- On login/register: Local ledger data is synced to user's cloud storage

### Data Files Structure
```
data/
├── users/
│   └── users.txt          # User credentials
└── ledgers/
    ├── local_accounts_{ledger_name}.csv    # Guest mode ledgers
    ├── {username}_accounts_{ledger_name}.csv # User ledgers (cloud)
    └── {username}_settings.txt             # User settings (limits, goals, ledger list)
```

## Future Implementation Notes
- Remember to implement ledger selection/creation UI
- Statistics should be per-ledger and aggregated
- Settings should support per-ledger limits and goals

