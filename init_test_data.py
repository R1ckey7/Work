"""
初始化测试数据脚本
用于创建测试账户和账本数据
作者: Rickey
日期: 30.10.2025
"""

from control.user_service import UserService
from control.ledger_service import LedgerService
from datetime import datetime


def init_test_data():
    """
    初始化测试数据
    创建测试账户和对应的账本
    """
    print("Initializing test data...\n")
    
    user_service = UserService()
    ledger_service = LedgerService()
    
    # 测试账户配置: (用户名, 密码)
    test_users = [
        ('zhangsan', '123456'),
        ('lisi', 'password'),
        ('wangwu', 'qwerty'),
    ]
    
    # 为每个账户创建账本配置: (账本名, 币种)
    ledger_configs = [
        ('default', 'AUD'),
        ('tourism', 'USD'),
        ('household', 'CNY'),
    ]
    
    # 创建测试账户
    print("Creating test accounts...")
    for username, password in test_users:
        try:
            # 检查用户是否已存在
            if user_service.user_exists(username):
                print(f"[SKIP] User '{username}' already exists")
                continue
            
            # 注册用户
            if user_service.register_user(username, password):
                print(f"[OK] Created user: {username}")
            else:
                print(f"[FAIL] Failed to create user: {username}")
        except Exception as e:
            print(f"[ERROR] Error creating user {username}: {e}")
    
    print("\nCreating test ledgers and data...")
    
    # 为每个账户创建账本并添加测试数据
    for username, password in test_users:
        for ledger_name, currency in ledger_configs:
            try:
                # 检查账本是否已存在
                if ledger_service.ledger_exists(ledger_name, username):
                    print(f"[SKIP] Ledger '{ledger_name}' ({currency}) already exists (User: {username})")
                    continue
                
                # 创建账本
                ledger = ledger_service.create_ledger(ledger_name, currency, username)
                print(f"[OK] Created ledger: {ledger_name} ({currency}) for {username}")
                
                # 添加测试支出数据
                test_expenses = [
                    {'year': 2025, 'month': 1, 'day': 15, 'amount': 50.00, 'category': 'food', 'description': 'Lunch'},
                    {'year': 2025, 'month': 1, 'day': 20, 'amount': 25.50, 'category': 'transportation', 'description': 'Bus ticket'},
                    {'year': 2025, 'month': 2, 'day': 5, 'amount': 100.00, 'category': 'shopping', 'description': 'Shopping'},
                    {'year': 2025, 'month': 2, 'day': 12, 'amount': 80.00, 'category': 'entertainment', 'description': 'Movie'},
                    {'year': 2025, 'month': 3, 'day': 3, 'amount': 150.00, 'category': 'bills', 'description': 'Electricity bill'},
                ]
                
                for expense in test_expenses:
                    iso_date = f"{expense['year']}-{expense['month']:02d}-{expense['day']:02d}"
                    ledger_service.add_expense(
                        ledger,
                        iso_date,
                        expense['amount'],
                        expense['category'],
                        expense['description']
                    )
                
                # 添加测试收入数据
                test_income = [
                    {'year': 2025, 'month': 1, 'day': 1, 'amount': 5000.00, 'category': 'salary', 'description': 'Monthly salary'},
                    {'year': 2025, 'month': 1, 'day': 15, 'amount': 500.00, 'category': 'bonus', 'description': 'Bonus'},
                    {'year': 2025, 'month': 2, 'day': 1, 'amount': 5000.00, 'category': 'salary', 'description': 'Monthly salary'},
                    {'year': 2025, 'month': 2, 'day': 28, 'amount': 200.00, 'category': 'gift', 'description': 'Gift'},
                ]
                
                for income in test_income:
                    iso_date = f"{income['year']}-{income['month']:02d}-{income['day']:02d}"
                    ledger_service.add_income(
                        ledger,
                        iso_date,
                        income['amount'],
                        income['category'],
                        income['description']
                    )
                
                print(f"[OK] Added test data for {ledger_name}")
                
            except Exception as e:
                print(f"[ERROR] Error creating ledger {ledger_name} for {username}: {e}")
    
    print("\n[DONE] Test data initialization completed!")


if __name__ == "__main__":
    try:
        init_test_data()
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        import traceback
        traceback.print_exc()

