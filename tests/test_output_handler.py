"""REQUIRED MODULE DOCUMENTATION"""

from unittest import TestCase, main
from output_handler.output_handler import OutputHandler

__author__ = ""
__version__ = ""

class TestOutputHandler(TestCase):
    """Defines the unit tests for the OutputHandler class."""

    def setUp(self):
        """This function is invoked before executing a unit test
        function.

        The following class attributes have been provided to reduce the 
        amount of code needed when creating OutputHandler class objects 
        in the tests that follow.  
        
        Example:
            >>> OutputHandler(self.account_summaries, 
                              self.suspicious_transactions, 
                              self.transaction_statistics)
        """
        self.account_summaries = { 
            "1001": {
                "account_number": "1001", 
                "balance": 50, 
                "total_deposits": 100, 
                "total_withdrawals": 50
            },
            "1002": {
                "account_number": "2", 
                "balance": 200, 
                "total_deposits": 200, 
                "total_withdrawals": 0
            }
        }

        self.suspicious_transactions = [
            {
                "Transaction ID": "1",
                "Account number": "1001",
                "Date": "2023-03-14",
                "Transaction type": "deposit",
                "Amount": 250,
                "Currency": "XRP",
                "Description": "crypto investment"
            }
        ]

        self.transaction_statistics = {
            "deposit": {
                "total_amount": 300, 
                "transaction_count": 2
            }, 
            "withdrawal": {
                "total_amount": 50, 
                "transaction_count": 1
            }
        }

    # Define unit test functions below

if __name__ == "__main__":
    main()
