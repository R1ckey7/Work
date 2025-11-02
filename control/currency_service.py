"""
Currency Service Class
Handles currency conversion operations

Author: Rickey
Date: 2025.10.22
"""

from datetime import datetime


class CurrencyService:
    """Service class for handling currency conversions"""
    
    # Base currency: AUD (Australian Dollar)
    # 相对于 AUD 的汇率 (1 AUD = X 其他货币)
    # 注意: 这些是示例汇率，生产环境应该更新为实时数据
    EXCHANGE_RATES = {
        'AUD': 1.0,      # 基础货币 (澳元)
        'USD': 0.65,     # 1 AUD = 0.65 USD
        'CNY': 4.70,     # 1 AUD = 4.70 CNY
        'EUR': 0.60,     # 1 AUD = 0.60 EUR
        'GBP': 0.52,     # 1 AUD = 0.52 GBP
        'JPY': 98.50,    # 1 AUD = 98.50 JPY
        'CAD': 0.89,     # 1 AUD = 0.89 CAD
        'HKD': 5.08      # 1 AUD = 5.08 HKD
    }
    
    def __init__(self):
        """初始化 CurrencyService"""
        self.base_currency = 'AUD'
        self.last_updated = datetime.now()
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        获取从一种货币到另一种货币的汇率
        
        参数:
            from_currency: 源货币代码
            to_currency: 目标货币代码
            
        返回:
            汇率（每单位源货币可兑换的目标货币数量）
            
        抛出:
            ValueError: 如果货币代码不受支持
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency not in self.EXCHANGE_RATES:
            raise ValueError(f"不支持的源货币: {from_currency}")
        
        if to_currency not in self.EXCHANGE_RATES:
            raise ValueError(f"不支持的目标货币: {to_currency}")
        
        # 通过基础货币 (AUD) 转换
        # 汇率 = (1单位源货币的AUD值) / (1单位目标货币的AUD值)
        from_rate = self.EXCHANGE_RATES[from_currency]
        to_rate = self.EXCHANGE_RATES[to_currency]
        
        # 汇率: 每1单位源货币可兑换多少单位目标货币
        exchange_rate = to_rate / from_rate
        
        return exchange_rate
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        将金额从一种货币转换为另一种货币
        
        参数:
            amount: 要转换的金额
            from_currency: 源货币代码
            to_currency: 目标货币代码
            
        返回:
            转换后的目标货币金额
            
        抛出:
            ValueError: 如果货币代码不受支持
        """
        if amount < 0:
            raise ValueError("金额不能为负数")
        
        if from_currency.upper() == to_currency.upper():
            return amount
        
        exchange_rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * exchange_rate
        
        return round(converted_amount, 2)
    
    def get_supported_currencies(self) -> list:
        """
        获取支持的货币代码列表
        
        返回:
            支持的货币代码列表
        """
        return list(self.EXCHANGE_RATES.keys())
    
    def is_currency_supported(self, currency: str) -> bool:
        """
        检查货币是否受支持
        
        参数:
            currency: 要检查的货币代码
            
        返回:
            支持返回 True，否则返回 False
        """
        return currency.upper() in self.EXCHANGE_RATES
    
    def update_exchange_rate(self, currency: str, rate_to_aud: float):
        """
        更新货币的汇率（相对于 AUD）
        
        参数:
            currency: 货币代码
            rate_to_aud: 汇率 (1单位货币 = rate_to_aud AUD)
            
        抛出:
            ValueError: 如果货币代码不受支持
        """
        currency = currency.upper()
        
        if currency == 'AUD':
            raise ValueError("无法更新 AUD 汇率（基础货币）")
        
        if currency not in self.EXCHANGE_RATES:
            raise ValueError(f"不支持的货币: {currency}")
        
        if rate_to_aud <= 0:
            raise ValueError("汇率必须为正数")
        
        self.EXCHANGE_RATES[currency] = rate_to_aud
        self.last_updated = datetime.now()
    
    def get_rate_info(self, currency: str) -> dict:
        """
        获取货币汇率信息
        
        参数:
            currency: 货币代码
            
        返回:
            包含汇率信息的字典
            
        抛出:
            ValueError: 如果货币代码不受支持
        """
        if not self.is_currency_supported(currency):
            raise ValueError(f"不支持的货币: {currency}")
        
        currency = currency.upper()
        rate_to_aud = self.EXCHANGE_RATES[currency]
        
        return {
            'currency': currency,
            'rate_to_aud': rate_to_aud,
            'rate_from_aud': round(1.0 / rate_to_aud, 4) if currency != 'AUD' else 1.0,
            'last_updated': self.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def convert_multiple(self, amounts: dict, to_currency: str) -> dict:
        """
        将多个金额（不同货币）转换为单一目标货币
        
        参数:
            amounts: 货币代码到金额的字典映射
                    示例: {'USD': 100, 'EUR': 50, 'CNY': 200}
            to_currency: 目标货币代码
            
        返回:
            包含转换后金额和总计的字典
            
        抛出:
            ValueError: 如果任何货币代码不受支持
        """
        if not self.is_currency_supported(to_currency):
            raise ValueError(f"不支持的目标货币: {to_currency}")
        
        converted = {}
        total = 0.0
        
        for currency, amount in amounts.items():
            if amount == 0:
                converted[currency] = 0.0
                continue
            
            converted_amount = self.convert(amount, currency, to_currency)
            converted[currency] = converted_amount
            total += converted_amount
        
        return {
            'converted_amounts': converted,
            'total': round(total, 2),
            'target_currency': to_currency.upper()
        }
