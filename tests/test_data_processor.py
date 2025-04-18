"""Unit tests for the data_processor.py.
There are tests for account summary updates, suspicious transactions,
and updatate transaction statistics that are in the DataProcessor class.
"""

import unittest
from unittest import TestCase
from data_processor.data_processor import DataProcessor

__author__ = "Muhammad Rahmani"
__version__ = "18-April-2025"

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
        
        self.regular_deposit = {
            "Transaction ID": "1",
            "Account number": "1001",
            "Date": "2023-03-01",
            "Transaction type": "deposit",
            "Amount": 1000,
            "Currency": "CAD",
            "Description": "Salary"
        } 
        self.large_deposit ={
            "Transaction ID": "2",
            "Account number": "1001",
            "Date": "2023-03-01",
            "Transaction type": "deposit",
            "Amount": 15000,
            "Currency": "CAD",
            "Description": "Salary"
        }
        self.uncommon_currency ={
            "Transaction ID": "3",
            "Account number": "1001",
            "Date": "2023-03-01",
            "Transaction type": "withdrawal",
            "Amount": 2000,
            "Currency": "XRP",
            "Description": "Crypto"
        }
        self.regular_withdrawal ={
            "Transaction ID": "4",
            "Account number": "1001",
            "Date": "2023-03-01",
            "Transaction type": "withdrawal",
            "Amount": 200,
            "Currency": "CAD",
            "Description": "ATM"
        }


    # Define unit test functions below

    def test_update_account_summary_deposit(self):
        """This tests to see if deposit for update
        account summary works as intended
        """
        # Arrange
        processor = DataProcessor([])

        # Act
        processor.update_account_summary(self.regular_deposit)

        # Assert
        account = processor.account_summaries["1001"]
        self.assertEqual(account["balance"], 1000)
        self.assertEqual(account["total_deposits"], 1000)
        self.assertEqual(account["total_withdrawals"], 0)

    def test_update_account_summary_withdrawal(self):
        """This tests to see if withdrawal for update
        account summary works as intended
        """
        # Arrange
        processor = DataProcessor([])
        processor.update_account_summary(self.regular_deposit)

        # Act
        processor.update_account_summary(self.regular_withdrawal)

        # Assert
        account = processor.account_summaries["1001"]
        self.assertEqual(account["balance"], 800)
        self.assertEqual(account["total_deposits"], 1000)
        self.assertEqual(account["total_withdrawals"], 200)

    def test_check_suspicious_large_amount(self):
        """This test checks to see if the transaction amount
        is greater than 10,000 dollars.
        """
        # Arrange
        processor = DataProcessor([])

        # Act
        processor.check_suspicious_transactions(self.large_deposit)

        # Assert
        self.assertIn(self.large_deposit, processor.suspicious_transactions)

    def test_check_suspicious_uncommon_currency(self):
        """This test checks to see if the transaction currency
        is uncommon.
        """
        # Arrange
        processor = DataProcessor([])

        # Act
        processor.check_suspicious_transactions(self.uncommon_currency)

        # Assert
        self.assertIn(self.uncommon_currency, processor.suspicious_transactions)

    def test_check_not_suspicious(self):
        """Tests to see if the transaction is NOT a suspicious transaction
        """
        # Arrange
        processor = DataProcessor([])

        # Act
        processor.check_suspicious_transactions(self.regular_deposit)

        # Assert
        self.assertNotIn(self.regular_deposit, processor.suspicious_transactions)

    def test_update_statistics_existing_type(self):
        """Tests the update statistics for existing type
        """
        # Arrange
        processor = DataProcessor([self.regular_deposit])
        processor.process_data()

        # Act
        processor.update_transaction_statistics(self.regular_deposit)

        # Assert
        statistics = processor.transaction_statistics["deposit"]
        self.assertEqual(statistics["total_amount"], 2000)
        self.assertEqual(statistics["transaction_count"], 2)

    def test_update_statistics_not_existing_type(self):
        """Tests the update statistics for non existing
        type.
        """
        # Arrange
        processor = DataProcessor([])

        # Act
        processor.update_transaction_statistics(self.regular_deposit)

        # Assert
        statistics = processor.transaction_statistics["deposit"]
        self.assertEqual(statistics["total_amount"], 1000)
        self.assertEqual(statistics["transaction_count"], 1)


if __name__ == "__main__":
    unittest.main()
