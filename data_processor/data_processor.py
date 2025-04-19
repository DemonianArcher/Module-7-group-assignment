"""The DataProcessor class processes financial transactions. The transactions
are added into the transaction list. The transaction list contains dictionaries
of the transactions data information.
The methods in DataProcessor class also check for suspicious transactions,
generates account sumaries and also computes transaction statistics.
"""

__author__ = "Muhammad Rahmani"
__version__ = "17-April-2025"

class DataProcessor:
    """The data processor class processes financial transaction
    data.
    """

    LARGE_TRANSACTION_THRESHOLD = 10000
    """LARGE_TRANSACTION_THRESHOLD sets a threshold of 10000 dollars.
    Any amount above this threshold is then added to the 
    suspicious_transactions list
    """

    UNCOMMON_CURRENCIES = ["XRP", "LTC"]
    """If the currencies in the UNCOMMON_CURRENCIES list is found, then
    those currencies are added to the suspicious_transactions list
    """

    def __init__(self, transactions: list):
        """This __init__ method initializes transactions for the class
        DataProcessor.

        Args:
            transactions (list): A list of dictionaries that contains
            transaction data. Each transaction in the dictionary contains
            the account number, transaction type, amount and currency.
        """

        self.__transactions = transactions
        self.__account_summaries = {}
        self.__suspicious_transactions = []
        self.__transaction_statistics = {}

    @property
    def input_data(self) -> list:
        """Gets the transaction data
        
        Returns:
                list: List of transaction dictionaries
        """
        

        return self.__transactions
    
    @property
    def account_summaries(self) -> dict:
        """Gets the account summary data

        Returns:
                dict: Returns the account data with keys:
                      account_number
                      balance
                      total_deposits
                      total_withdrawals
        """

        return self.__account_summaries
    
    @property
    def suspicious_transactions(self) -> list:
        """Gets the list of suspicious transactions
        
        Returns:
                list: Returns the list of suspicious
                transactions, which are amount above
                10,000 dollars threshold and the uncommon
                currencies.
        """

        return self.__suspicious_transactions
    
    @property
    def transaction_statistics(self) -> dict:
        """Gets the transaction statistics.
        
        Returns:
                dict: Transaction statistics for transaction type
                which contains the total_amount and transaction_count.
        """

        return self.__transaction_statistics

    def process_data(self) -> dict:
        """This function processes data and then returns account and
        transaction information. Updates the account summaries, checks
        for suspicious transactions and updates the transaction statistics.

        Returns:
               dict: Returns dictionary containing amount summary,
                     suspicious transactions, and transaction statistics.
        """

        for transaction in self.__transactions:
            self.update_account_summary(transaction)
            self.check_suspicious_transactions(transaction)
            self.update_transaction_statistics(transaction)

        return {"account_summaries": self.__account_summaries,
                "suspicious_transactions": self.__suspicious_transactions,
                "transaction_statistics": self.__transaction_statistics}

    def update_account_summary(self, transaction: dict) -> None:
        """This method checks for account number if it is not in account
        summaries dictionary, then it adds it to the account summaries
        dictionary. It also checks to see if the transaction type is deposit
        then it adds the amount to balance and total deposits. Similarly
        if the transaction type is withdrawal it subtracts from balance
        and adds to total withdrawals.

        Args:
             transaction (dict): The transaction data dictionary
        """

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
        """This method checks to see if amount is above the threshold 10,000
        dollars and checks to see if the currency is uncommon.

        Args:
             transaction (dict): The transaction data dictionary
        """

        amount = float(transaction["Amount"])
        currency = transaction["Currency"]

        if amount > self.LARGE_TRANSACTION_THRESHOLD \
            or currency in self.UNCOMMON_CURRENCIES:
            self.__suspicious_transactions.append(transaction)

    def update_transaction_statistics(self, transaction: dict) -> None:
        """This method checks to see if a transaction type is not in 
        transaction statistics, it assigns the total amount and transaction
        count the value of 0. Otherwise it adds the amount to total amount
        and plus 1 to the transaction count.

        Args:
             transaction (dict): The transaction data dictionary
        """

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
        """This method calculates the average transaction amount for a transaction
        type. It returns 0 if the transaction cost is 0 otherwise it returns the average
        transaction amount.

        Args:
             transaction_type (str): The transaction type either withdrawal or deposit.

        Returns:
                float: If the transaction count is 0 then it returns 0, otherwise it
                returns the average transaction amount.
        """
        
        total_amount = self.__transaction_statistics[transaction_type]["total_amount"]
        transaction_count = self.__transaction_statistics[transaction_type]["transaction_count"]
    
        return 0 if transaction_count == 0 else total_amount / transaction_count
