"""REQUIRED MODULE DOCUMENTATION"""

__author__ = ""
__version__ = ""

class DataProcessor:
    """REQUIRED: CLASS DOCSTRING"""

    LARGE_TRANSACTION_THRESHOLD = 10000
    """REQUIRED CLASS FIELD DOCUMENTATION"""

    UNCOMMON_CURRENCIES = ["XRP", "LTC"]
    """REQUIRED CLASS FIELD DOCUMENTATION"""

    def __init__(self, transactions: list):
        """REQUIRED: METHOD DOCSTRING"""

        self.__transactions = transactions
        self.__account_summaries = {}
        self.__suspicious_transactions = []
        self.__transaction_statistics = {}

    @property
    def input_data(self) -> list:
        """REQUIRED: METHOD DOCSTRING"""

        return self.__transactions
    
    @property
    def account_summaries(self) -> dict:
        """REQUIRED: METHOD DOCSTRING"""

        return self.__account_summaries
    
    @property
    def suspicious_transactions(self) -> list:
        """REQUIRED: METHOD DOCSTRING"""

        return self.__suspicious_transactions
    
    @property
    def transaction_statistics(self) -> dict:
        """REQUIRED: METHOD DOCSTRING"""

        return self.__transaction_statistics

    def process_data(self) -> dict:
        """REQUIRED: METHOD DOCSTRING"""

        for transaction in self.__transactions:
            self.update_account_summary(transaction)
            self.check_suspicious_transactions(transaction)
            self.update_transaction_statistics(transaction)

        return {"account_summaries": self.__account_summaries,
                "suspicious_transactions": self.__suspicious_transactions,
                "transaction_statistics": self.__transaction_statistics}

    def update_account_summary(self, transaction: dict) -> None:
        """REQUIRED: METHOD DOCSTRING"""

        account_number = transaction["Account number"]
        transaction_type = transaction["Transaction type"]
        amount = float(transaction["Amount"])

        if account_number not in self.__account_summaries:
            self.__account_summaries[account_number] = {
                "account_number": account_number,
                "balance": 0,
                "total_deposits": 0,
                "total_withdrawals": 0
            }

        if transaction_type == "deposit":
            self.__account_summaries[account_number]["balance"] += amount
            self.__account_summaries[account_number]["total_deposits"] += amount
        elif transaction_type == "withdrawal":
            self.__account_summaries[account_number]["balance"] -= amount
            self.__account_summaries[account_number]["total_withdrawals"] += amount

    def check_suspicious_transactions(self, transaction: dict) -> None:
        """REQUIRED: METHOD DOCSTRING"""

        amount = float(transaction["Amount"])
        currency = transaction["Currency"]

        if amount > self.LARGE_TRANSACTION_THRESHOLD \
            or currency in self.UNCOMMON_CURRENCIES:
            self.__suspicious_transactions.append(transaction)

    def update_transaction_statistics(self, transaction: dict) -> None:
        """REQUIRED: METHOD DOCSTRING"""

        transaction_type = transaction["Transaction type"]
        amount = float(transaction["Amount"])

        if transaction_type not in self.__transaction_statistics:
            self.__transaction_statistics[transaction_type] = {
                "total_amount": 0,
                "transaction_count": 0
            }

        self.__transaction_statistics[transaction_type]["total_amount"] += amount
        self.__transaction_statistics[transaction_type]["transaction_count"] += 1

    def get_average_transaction_amount(self, transaction_type: str) -> float:
        """REQUIRED: METHOD DOCSTRING"""
        
        total_amount = self.__transaction_statistics[transaction_type]["total_amount"]
        transaction_count = self.__transaction_statistics[transaction_type]["transaction_count"]
    
        return 0 if transaction_count == 0 else total_amount / transaction_count
