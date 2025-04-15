"""REQUIRED MODULE DOCUMENTATION"""

import unittest
from unittest import TestCase
from data_processor.data_processor import DataProcessor

__author__ = ""
__version__ = ""

class TestDataProcessor(TestCase):
    """Defines the unit tests for the DataProcessor class."""

    def setUp(self):
        """This function is invoked before executing a unit test
        function.

        The following class attribute has been provided to reduce the 
        amount of code needed when creating DataProcessor class objects 
        in the tests that follow.  
        
        Example:
            >>> data_processor = DataProcessor(self.transactions)
        """
        self.transactions = [
            {
                "Transaction ID": "1",
                "Account number": "1001",
                "Date": "2023-03-01",
                "Transaction type": "deposit",
                "Amount": 1000,
                "Currency": "CAD",
                "Description": "Salary"
            }, 
            {
                "Transaction ID": "2",
                "Account number": "1002",
                "Date": "2023-03-01",
                "Transaction type": "deposit",
                "Amount": 1500,
                "Currency": "CAD",
                "Description": "Salary"
            }
        ]

    # Define unit test functions below

if __name__ == "__main__":
    unittest.main()
