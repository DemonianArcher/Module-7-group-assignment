"""
Unit Tests for InputHandler Module

This module contains unit tests for the `InputHandler` class, which is responsible for 
handling input files in CSV and JSON formats. The tests ensure that the methods in 
the `InputHandler` class function as expected.

Tested Methods:
    - get_file_format: Verifies the file format based on the file extension.
    - read_csv_data: Ensures data is correctly read from a CSV file and raises 
      appropriate exceptions for invalid files.
    - read_input_data: Tests reading data from both CSV and JSON files and handles 
      unsupported file formats.

Classes:
    InputHandlerTests: Defines the unit tests for the `InputHandler` class.

Author: Avery Cloutier
Version: 1.0
"""

import os
import unittest
from unittest import TestCase
from input_handler.input_handler import InputHandler

__author__ = ""
__version__ = ""

class InputHandlerTests(TestCase):
    """Defines the unit tests for the InputHandler class."""

    def setUp(self):
        """
        This function is invoked before executing a unit test function.

        Sets up temporary file paths for testing purposes.
        """
        self.csv_file_path = "test_input.csv"
        self.json_file_path = "test_input.json"
        self.invalid_file_path = "invalid_file.txt"

        # Create a temporary CSV file for testing
        with open(self.csv_file_path, "w") as csv_file:
            csv_file.write(
                "Transaction ID,Account number,Date,Transaction type,Amount,Currency,Description\n"
                "1,1001,2023-03-01,deposit,1000,CAD,Salary\n"
                "2,1002,2023-03-01,deposit,1500,CAD,Salary\n"
            )

        # Create a temporary JSON file for testing
        with open(self.json_file_path, "w") as json_file:
            json_file.write(
                '[{"Transaction ID": "1", "Account number": "1001", "Date": "2023-03-01", '
                '"Transaction type": "deposit", "Amount": "1000", "Currency": "CAD", "Description": "Salary"}, '
                '{"Transaction ID": "2", "Account number": "1002", "Date": "2023-03-01", '
                '"Transaction type": "deposit", "Amount": "1500", "Currency": "CAD", "Description": "Salary"}]'
            )

    def tearDown(self):
        """
        This function is invoked after executing a unit test function.

        Cleans up temporary files created for testing purposes.
        """
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)
        if os.path.exists(self.json_file_path):
            os.remove(self.json_file_path)

    def test_get_file_format(self):
        """Tests the get_file_format method."""
        handler = InputHandler(self.csv_file_path)
        self.assertEqual(handler.get_file_format(), "csv")

        handler = InputHandler(self.json_file_path)
        self.assertEqual(handler.get_file_format(), "json")

        handler = InputHandler(self.invalid_file_path)
        self.assertEqual(handler.get_file_format(), "txt")

    def test_read_csv_data(self):
        """Tests the read_csv_data method."""
        handler = InputHandler(self.csv_file_path)
        transactions = handler.read_csv_data()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["Transaction ID"], "1")
        self.assertEqual(transactions[1]["Transaction type"], "deposit")

        # Test for FileNotFoundError
        handler = InputHandler("non_existent_file.csv")
        with self.assertRaises(FileNotFoundError):
            handler.read_csv_data()

    def test_read_input_data(self):
        """Tests the read_input_data method."""
        # Test for CSV file
        handler = InputHandler(self.csv_file_path)
        transactions = handler.read_input_data()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["Transaction ID"], "1")

        # Test for JSON file
        handler = InputHandler(self.json_file_path)
        transactions = handler.read_input_data()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[1]["Account number"], "1002")

        # Test for unsupported file format
        handler = InputHandler(self.invalid_file_path)
        with self.assertRaises(ValueError):
            handler.read_input_data()

    def test_data_validation(self):
        """Tests the data_validation method."""
        handler = InputHandler("dummy_path")

        # Define validation rules
        validation_rules = {
            'required_keys': {'Transaction ID', 'Account number', 'Date', 'Transaction type', 'Amount', 'Currency', 'Description'},
            'valid_transaction_types': {'deposit', 'withdrawal', 'transfer'}
        }

        # Define test transactions
        transactions = [
            {"Transaction ID": "1", "Account number": "1001", "Date": "2023-03-01", "Transaction type": "deposit", "Amount": "1000", "Currency": "CAD", "Description": "Salary"},
            {"Transaction ID": "2", "Account number": "1002", "Date": "2023-03-01", "Transaction type": "withdrawal", "Amount": "-500", "Currency": "CAD", "Description": "Groceries"},
            {"Transaction ID": "3", "Account number": "1003", "Date": "2023-03-02", "Transaction type": "invalid_type", "Amount": "200", "Currency": "CAD", "Description": "Shopping"},
            {"Transaction ID": "4", "Account number": "1004", "Date": "2023-03-03", "Transaction type": "transfer", "Amount": "abc", "Currency": "CAD", "Description": "Transfer to Savings"},
            {"Transaction ID": "5", "Account number": "1005", "Date": "2023-03-04", "Transaction type": "deposit", "Amount": "1500", "Currency": "CAD", "Description": "Bonus"}
        ]

        # Validate transactions
        valid_transactions = handler.data_validation(transactions, validation_rules)

        # Expected valid transactions
        expected_transactions = [
            {"Transaction ID": "1", "Account number": "1001", "Date": "2023-03-01", "Transaction type": "deposit", "Amount": "1000", "Currency": "CAD", "Description": "Salary"},
            {"Transaction ID": "5", "Account number": "1005", "Date": "2023-03-04", "Transaction type": "deposit", "Amount": "1500", "Currency": "CAD", "Description": "Bonus"}
        ]

        # Assertions
        self.assertEqual(valid_transactions, expected_transactions)
        self.assertEqual(len(valid_transactions), 2)
        self.assertNotIn({"Transaction ID": "2", "Account number": "1002", "Date": "2023-03-01", "Transaction type": "withdrawal", "Amount": "-500", "Currency": "CAD", "Description": "Groceries"}, valid_transactions)
        self.assertNotIn({"Transaction ID": "3", "Account number": "1003", "Date": "2023-03-02", "Transaction type": "invalid_type", "Amount": "200", "Currency": "CAD", "Description": "Shopping"}, valid_transactions)
        self.assertNotIn({"Transaction ID": "4", "Account number": "1004", "Date": "2023-03-03", "Transaction type": "transfer", "Amount": "abc", "Currency": "CAD", "Description": "Transfer to Savings"}, valid_transactions)


if __name__ == "__main__":
    unittest.main()
