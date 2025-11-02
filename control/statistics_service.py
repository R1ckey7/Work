"""
Statistics Service Class
Handles financial statistics and reporting

Author: Rickey
Date: 2025.10.24
"""

from datetime import datetime
from control.ledger_service import LedgerService
from model.ledger import Ledger


class StatisticsService:
    """Service class for handling statistics operations"""
    
    def __init__(self):
        """初始化 StatisticsService"""
        self.ledger_service = LedgerService()
    
    def get_expenses_by_year(self, ledger: Ledger, year: int) -> dict:
        """
        获取特定年份的支出统计
        
        参数:
            ledger: 账本对象
            year: 年份（如 2025）
            
        返回:
            包含总支出和按类别分组的支出的字典
        """
        expenses = self.ledger_service.get_expenses(ledger)
        
        total = 0.0
        by_category = {}
        
        for expense in expenses:
            try:
                expense_year = int(expense['year'])
                if expense_year == year:
                    amount = float(expense['amount'])
                    category = expense['category']
                    
                    total += amount
                    
                    if category in by_category:
                        by_category[category] += amount
                    else:
                        by_category[category] = amount
            except (ValueError, KeyError):
                continue
        
        # 四舍五入金额
        total = round(total, 2)
        for category in by_category:
            by_category[category] = round(by_category[category], 2)
        
        return {
            'total': total,
            'by_category': by_category,
            'year': year
        }
    
    def get_expenses_by_month(self, ledger: Ledger, year: int, month: int) -> dict:
        """
        获取特定月份的支出统计
        
        参数:
            ledger: 账本对象
            year: 年份（如 2025）
            month: 月份（1-12）
            
        返回:
            包含总支出和按类别分组的支出的字典
        """
        expenses = self.ledger_service.get_expenses(ledger)
        
        total = 0.0
        by_category = {}
        
        for expense in expenses:
            try:
                expense_year = int(expense['year'])
                expense_month = int(expense['month'])
                if expense_year == year and expense_month == month:
                    amount = float(expense['amount'])
                    category = expense['category']
                    
                    total += amount
                    
                    if category in by_category:
                        by_category[category] += amount
                    else:
                        by_category[category] = amount
            except (ValueError, KeyError):
                continue
        
        # 四舍五入金额
        total = round(total, 2)
        for category in by_category:
            by_category[category] = round(by_category[category], 2)
        
        return {
            'total': total,
            'by_category': by_category,
            'year': year,
            'month': month
        }
    
    def get_expenses_by_date(self, ledger: Ledger, year: int, month: int, day: int) -> list:
        """
        获取特定日期的支出记录
        
        参数:
            ledger: 账本对象
            year: 年份（如 2025）
            month: 月份（1-12）
            day: 日期（1-31）
            
        返回:
            该日期的支出记录列表
        """
        expenses = self.ledger_service.get_expenses(ledger)
        
        result = []
        for expense in expenses:
            try:
                expense_year = int(expense['year'])
                expense_month = int(expense['month'])
                expense_day = int(expense['day'])
                
                if expense_year == year and expense_month == month and expense_day == day:
                    result.append(expense)
            except (ValueError, KeyError):
                continue
        
        return result
    
    def get_income_by_year(self, ledger: Ledger, year: int) -> dict:
        """
        获取特定年份的收入统计
        
        参数:
            ledger: 账本对象
            year: 年份（如 2025）
            
        返回:
            包含总收入和按类别分组的收入的字典
        """
        income = self.ledger_service.get_income(ledger)
        
        total = 0.0
        by_category = {}
        
        for inc in income:
            try:
                inc_year = int(inc['year'])
                if inc_year == year:
                    amount = float(inc['amount'])
                    category = inc['category']
                    
                    total += amount
                    
                    if category in by_category:
                        by_category[category] += amount
                    else:
                        by_category[category] = amount
            except (ValueError, KeyError):
                continue
        
        # 四舍五入金额
        total = round(total, 2)
        for category in by_category:
            by_category[category] = round(by_category[category], 2)
        
        return {
            'total': total,
            'by_category': by_category,
            'year': year
        }
    
    def get_income_by_month(self, ledger: Ledger, year: int, month: int) -> dict:
        """
        获取特定月份的收入统计
        
        参数:
            ledger: 账本对象
            year: 年份（如 2025）
            month: 月份（1-12）
            
        返回:
            包含总收入和按类别分组的收入的字典
        """
        income = self.ledger_service.get_income(ledger)
        
        total = 0.0
        by_category = {}
        
        for inc in income:
            try:
                inc_year = int(inc['year'])
                inc_month = int(inc['month'])
                if inc_year == year and inc_month == month:
                    amount = float(inc['amount'])
                    category = inc['category']
                    
                    total += amount
                    
                    if category in by_category:
                        by_category[category] += amount
                    else:
                        by_category[category] = amount
            except (ValueError, KeyError):
                continue
        
        # 四舍五入金额
        total = round(total, 2)
        for category in by_category:
            by_category[category] = round(by_category[category], 2)
        
        return {
            'total': total,
            'by_category': by_category,
            'year': year,
            'month': month
        }
    
    def get_income_by_date(self, ledger: Ledger, year: int, month: int, day: int) -> list:
        """
        获取特定日期的收入记录
        
        参数:
            ledger: 账本对象
            year: 年份（如 2025）
            month: 月份（1-12）
            day: 日期（1-31）
            
        返回:
            该日期的收入记录列表
        """
        income = self.ledger_service.get_income(ledger)
        
        result = []
        for inc in income:
            try:
                inc_year = int(inc['year'])
                inc_month = int(inc['month'])
                inc_day = int(inc['day'])
                
                if inc_year == year and inc_month == month and inc_day == day:
                    result.append(inc)
            except (ValueError, KeyError):
                continue
        
        return result
