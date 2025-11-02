"""
Ledger Service Class
Handles ledger-related business logic including creation, reading, and writing

Author: Rickey
Date: 2025.10.19
"""

import os
import csv
from datetime import datetime
from model.ledger import Ledger


class LedgerService:
    """Service class for handling ledger operations"""
    
    # Common currency codes
    SUPPORTED_CURRENCIES = {
        'USD': 'US Dollar',
        'CNY': 'Chinese Yuan',
        'AUD': 'Australian Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'CAD': 'Canadian Dollar',
        'HKD': 'Hong Kong Dollar'
    }
    
    def __init__(self):
        """初始化 LedgerService"""
        self.base_path = "data/ledgers"
        self._ensure_base_directory()
    
    def _ensure_base_directory(self):
        """确保基础账本目录存在"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def create_default_ledger(self, username: str = None, currency: str = "AUD") -> Ledger:
        """
        为新用户或访客创建默认账本
        
        参数:
            username: 用户名（如果已登录），访客模式为 None
            currency: 货币代码（默认: AUD，适用于澳大利亚用户）
            
        返回:
            创建成功返回账本对象，已存在返回 None
        """
        try:
            ledger = self.create_ledger("default", currency, username)
            return ledger
        except FileExistsError:
            # 默认账本已存在，返回现有的
            if username:
                folder_path = f"{self.base_path}/{username}-default"
            else:
                folder_path = f"{self.base_path}/local-default"
            
            # 从现有文件读取货币信息
            expenses_path = f"{folder_path}/expenses.csv"
            if os.path.exists(expenses_path):
                with open(expenses_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline()
                    if first_line.startswith("# Currency:"):
                        currency = first_line.split(":")[1].strip()
            
            return Ledger("default", currency, username)
        except Exception as e:
            print(f"创建默认账本时出错: {e}")
            return None
    
    def create_ledger(self, ledger_name: str, currency: str, username: str = None) -> Ledger:
        """
        创建新账本，包含支出和收入 CSV 文件
        
        参数:
            ledger_name: 账本名称
            currency: 货币代码（如 USD, CNY, AUD）
            username: 用户名（如果已登录），访客模式为 None
            
        返回:
            创建成功返回账本对象，否则返回 None
        """
        # 验证货币
        if currency.upper() not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"不支持的货币: {currency}。支持的货币: {list(self.SUPPORTED_CURRENCIES.keys())}")
        
        # 创建账本对象
        ledger = Ledger(ledger_name, currency.upper(), username)
        folder_path = ledger.get_folder_path()
        
        # 检查账本是否已存在
        if os.path.exists(folder_path):
            raise FileExistsError(f"账本 '{ledger_name}' 已存在！")
        
        try:
            # 创建账本文件夹
            os.makedirs(folder_path)
            
            # 创建支出 CSV 文件并写入表头
            expenses_path = ledger.get_expenses_file_path()
            with open(expenses_path, 'w', newline='', encoding='utf-8') as f:
                # 将货币信息作为注释写入（第一行）
                f.write(f"# Currency: {currency.upper()}\n")
                # 写入 CSV 表头
                writer = csv.writer(f)
                writer.writerow(['year', 'month', 'day', 'amount', 'category', 'description'])
            
            # 创建收入 CSV 文件并写入表头
            income_path = ledger.get_income_file_path()
            with open(income_path, 'w', newline='', encoding='utf-8') as f:
                # 将货币信息作为注释写入（第一行）
                f.write(f"# Currency: {currency.upper()}\n")
                # 写入 CSV 表头
                writer = csv.writer(f)
                writer.writerow(['year', 'month', 'day', 'amount', 'category', 'description'])
            
            return ledger
            
        except Exception as e:
            # 如果创建失败则清理
            if os.path.exists(folder_path):
                import shutil
                shutil.rmtree(folder_path)
            raise Exception(f"创建账本失败: {e}")
    
    def add_expense(self, ledger: Ledger, date: str, amount: float, category: str, description: str = "") -> bool:
        """
        向账本添加支出记录
        
        参数:
            ledger: 账本对象
            date: 日期，YYYY-MM-DD 格式（ISO 格式，内部存储）
            amount: 支出金额
            category: 支出类别
            description: 可选描述
            
        返回:
            添加成功返回 True，否则返回 False
        """
        try:
            expenses_path = ledger.get_expenses_file_path()
            
            # 解析日期获取年、月、日
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            year = date_obj.year
            month = date_obj.month
            day = date_obj.day
            
            # 追加到 CSV
            with open(expenses_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([year, month, day, amount, category, description])
            
            return True
        except Exception as e:
            print(f"添加支出时出错: {e}")
            return False
    
    def add_income(self, ledger: Ledger, date: str, amount: float, category: str, description: str = "") -> bool:
        """
        向账本添加收入记录
        
        参数:
            ledger: 账本对象
            date: 日期，YYYY-MM-DD 格式（ISO 格式，内部存储）
            amount: 收入金额
            category: 收入类别
            description: 可选描述
            
        返回:
            添加成功返回 True，否则返回 False
        """
        try:
            income_path = ledger.get_income_file_path()
            
            # 解析日期获取年、月、日
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            year = date_obj.year
            month = date_obj.month
            day = date_obj.day
            
            # 追加到 CSV
            with open(income_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([year, month, day, amount, category, description])
            
            return True
        except Exception as e:
            print(f"添加收入时出错: {e}")
            return False
    
    def get_expenses(self, ledger: Ledger) -> list:
        """
        从账本获取所有支出记录
        
        参数:
            ledger: 账本对象
            
        返回:
            支出记录字典列表
        """
        expenses = []
        expenses_path = ledger.get_expenses_file_path()
        
        if not os.path.exists(expenses_path):
            return expenses
        
        try:
            with open(expenses_path, 'r', encoding='utf-8') as f:
                # 如果存在注释行则跳过
                first_line = f.readline()
                if first_line.startswith('#'):
                    # 注释行，正常读取
                    f.seek(0)
                    f.readline()  # 跳过注释
                
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('year'):  # 包含年份字段的有效行
                        expenses.append(row)
        except Exception as e:
            print(f"读取支出时出错: {e}")
        
        return expenses
    
    def get_income(self, ledger: Ledger) -> list:
        """
        从账本获取所有收入记录
        
        参数:
            ledger: 账本对象
            
        返回:
            收入记录字典列表
        """
        income = []
        income_path = ledger.get_income_file_path()
        
        if not os.path.exists(income_path):
            return income
        
        try:
            with open(income_path, 'r', encoding='utf-8') as f:
                # 如果存在注释行则跳过
                first_line = f.readline()
                if first_line.startswith('#'):
                    # 注释行，正常读取
                    f.seek(0)
                    f.readline()  # 跳过注释
                
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('year'):  # 包含年份字段的有效行
                        income.append(row)
        except Exception as e:
            print(f"读取收入时出错: {e}")
        
        return income
    
    def delete_expense(self, ledger: Ledger, index: int) -> bool:
        """
        通过索引删除支出记录
        
        参数:
            ledger: 账本对象
            index: 要删除的记录的从零开始的索引
            
        返回:
            删除成功返回 True，否则返回 False
        """
        try:
            expenses_path = ledger.get_expenses_file_path()
            
            if not os.path.exists(expenses_path):
                return False
            
            # 读取所有支出
            expenses = []
            currency_line = None
            
            with open(expenses_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line.startswith('#'):
                    currency_line = first_line
                    f.seek(0)
                    f.readline()  # 跳过注释
                
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('year'):
                        expenses.append(row)
            
            # 检查索引是否有效
            if index < 0 or index >= len(expenses):
                return False
            
            # 移除索引位置的支出
            expenses.pop(index)
            
            # 写回文件
            with open(expenses_path, 'w', newline='', encoding='utf-8') as f:
                if currency_line:
                    f.write(currency_line)
                writer = csv.writer(f)
                writer.writerow(['year', 'month', 'day', 'amount', 'category', 'description'])
                for expense in expenses:
                    writer.writerow([
                        expense['year'],
                        expense['month'],
                        expense['day'],
                        expense['amount'],
                        expense['category'],
                        expense.get('description', '')
                    ])
            
            return True
        except Exception as e:
            print(f"删除支出时出错: {e}")
            return False
    
    def delete_income(self, ledger: Ledger, index: int) -> bool:
        """
        通过索引删除收入记录
        
        参数:
            ledger: 账本对象
            index: 要删除的记录的从零开始的索引
            
        返回:
            删除成功返回 True，否则返回 False
        """
        try:
            income_path = ledger.get_income_file_path()
            
            if not os.path.exists(income_path):
                return False
            
            # 读取所有收入
            income = []
            currency_line = None
            
            with open(income_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line.startswith('#'):
                    currency_line = first_line
                    f.seek(0)
                    f.readline()  # 跳过注释
                
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('year'):
                        income.append(row)
            
            # 检查索引是否有效
            if index < 0 or index >= len(income):
                return False
            
            # 移除索引位置的收入
            income.pop(index)
            
            # 写回文件
            with open(income_path, 'w', newline='', encoding='utf-8') as f:
                if currency_line:
                    f.write(currency_line)
                writer = csv.writer(f)
                writer.writerow(['year', 'month', 'day', 'amount', 'category', 'description'])
                for inc in income:
                    writer.writerow([
                        inc['year'],
                        inc['month'],
                        inc['day'],
                        inc['amount'],
                        inc['category'],
                        inc.get('description', '')
                    ])
            
            return True
        except Exception as e:
            print(f"删除收入时出错: {e}")
            return False
    
    def update_expense(self, ledger: Ledger, index: int, date: str, amount: float, category: str, description: str = "") -> bool:
        """
        通过索引更新支出记录
        
        参数:
            ledger: 账本对象
            index: 要更新的记录的从零开始的索引
            date: 日期，YYYY-MM-DD 格式
            amount: 支出金额
            category: 支出类别
            description: 可选描述
            
        返回:
            更新成功返回 True，否则返回 False
        """
        try:
            expenses_path = ledger.get_expenses_file_path()
            
            if not os.path.exists(expenses_path):
                return False
            
            # 解析日期获取年、月、日
            from datetime import datetime
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            year = date_obj.year
            month = date_obj.month
            day = date_obj.day
            
            # 读取所有支出
            expenses = []
            currency_line = None
            
            with open(expenses_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line.startswith('#'):
                    currency_line = first_line
                    f.seek(0)
                    f.readline()  # 跳过注释
                
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('year'):
                        expenses.append(row)
            
            # 检查索引是否有效
            if index < 0 or index >= len(expenses):
                return False
            
            # 更新索引位置的支出
            expenses[index] = {
                'year': str(year),
                'month': str(month),
                'day': str(day),
                'amount': str(amount),
                'category': category,
                'description': description
            }
            
            # 写回文件
            with open(expenses_path, 'w', newline='', encoding='utf-8') as f:
                if currency_line:
                    f.write(currency_line)
                writer = csv.writer(f)
                writer.writerow(['year', 'month', 'day', 'amount', 'category', 'description'])
                for expense in expenses:
                    writer.writerow([
                        expense['year'],
                        expense['month'],
                        expense['day'],
                        expense['amount'],
                        expense['category'],
                        expense.get('description', '')
                    ])
            
            return True
        except Exception as e:
            print(f"更新支出时出错: {e}")
            return False
    
    def update_income(self, ledger: Ledger, index: int, date: str, amount: float, category: str, description: str = "") -> bool:
        """
        通过索引更新收入记录
        
        参数:
            ledger: 账本对象
            index: 要更新的记录的从零开始的索引
            date: 日期，YYYY-MM-DD 格式
            amount: 收入金额
            category: 收入类别
            description: 可选描述
            
        返回:
            更新成功返回 True，否则返回 False
        """
        try:
            income_path = ledger.get_income_file_path()
            
            if not os.path.exists(income_path):
                return False
            
            # 解析日期获取年、月、日
            from datetime import datetime
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            year = date_obj.year
            month = date_obj.month
            day = date_obj.day
            
            # 读取所有收入
            income = []
            currency_line = None
            
            with open(income_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line.startswith('#'):
                    currency_line = first_line
                    f.seek(0)
                    f.readline()  # 跳过注释
                
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('year'):
                        income.append(row)
            
            # 检查索引是否有效
            if index < 0 or index >= len(income):
                return False
            
            # 更新索引位置的收入
            income[index] = {
                'year': str(year),
                'month': str(month),
                'day': str(day),
                'amount': str(amount),
                'category': category,
                'description': description
            }
            
            # 写回文件
            with open(income_path, 'w', newline='', encoding='utf-8') as f:
                if currency_line:
                    f.write(currency_line)
                writer = csv.writer(f)
                writer.writerow(['year', 'month', 'day', 'amount', 'category', 'description'])
                for inc in income:
                    writer.writerow([
                        inc['year'],
                        inc['month'],
                        inc['day'],
                        inc['amount'],
                        inc['category'],
                        inc.get('description', '')
                    ])
            
            return True
        except Exception as e:
            print(f"更新收入时出错: {e}")
            return False
    
    def list_user_ledgers(self, username: str = None) -> list:
        """
        列出用户的所有账本
        
        参数:
            username: 用户名（如果已登录），访客模式为 None
            
        返回:
            Ledger 对象列表
        """
        ledgers = []
        
        if username:
            # 列出用户账本: 用户名-账本名
            prefix = f"{username}-"
        else:
            # 列出访客账本: local-账本名
            prefix = "local-"
        
        if not os.path.exists(self.base_path):
            return ledgers
        
        try:
            for item in os.listdir(self.base_path):
                item_path = os.path.join(self.base_path, item)
                if os.path.isdir(item_path) and item.startswith(prefix):
                    # 提取账本名称
                    ledger_name = item[len(prefix):]
                    
                    # 从支出文件读取货币信息
                    expenses_path = os.path.join(item_path, "expenses.csv")
                    currency = "USD"  # 默认值
                    
                    if os.path.exists(expenses_path):
                        with open(expenses_path, 'r', encoding='utf-8') as f:
                            first_line = f.readline()
                            if first_line.startswith("# Currency:"):
                                currency = first_line.split(":")[1].strip()
                    
                    ledger = Ledger(ledger_name, currency, username)
                    ledgers.append(ledger)
        except Exception as e:
            print(f"列出账本时出错: {e}")
        
        return ledgers
    
    def ledger_exists(self, ledger_name: str, username: str = None) -> bool:
        """
        检查账本是否存在
        
        参数:
            ledger_name: 账本名称
            username: 用户名（如果已登录），访客模式为 None
            
        返回:
            账本存在返回 True，否则返回 False
        """
        if username:
            folder_path = f"{self.base_path}/{username}-{ledger_name}"
        else:
            folder_path = f"{self.base_path}/local-{ledger_name}"
        
        return os.path.exists(folder_path)

