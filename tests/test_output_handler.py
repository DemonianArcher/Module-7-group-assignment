"""Unit tests for the OutputHandler class."""

import unittest
import csv
import os
from typing import List, Dict
from unittest import TestCase, mock
from output_handler.output_handler import OutputHandler

__author__ = "Sharef"
__version__ = "1.0"

class TestOutputHandler(TestCase):
    """Defines the unit tests for the OutputHandler class."""

    def setUp(self):
        """Set up test fixtures."""
        self.account_summaries = { 
            "1001": {
                "account_number": "1001", 
                "balance": 50, 
                "total_deposits": 100, 
                "total_withdrawals": 50
            },
            "1002": {
                "account_number": "1002", 
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

    def test_init(self):
        """Test OutputHandler initialization."""
        handler = OutputHandler(self.account_summaries,
                               self.suspicious_transactions,
                               self.transaction_statistics)
        self.assertIsInstance(handler, OutputHandler)

    def test_account_summaries_property(self):
        """Test account_summaries property returns correct data."""
        handler = OutputHandler(self.account_summaries,
                               self.suspicious_transactions,
                               self.transaction_statistics)
        self.assertEqual(handler.account_summaries, self.account_summaries)

    def test_suspicious_transactions_property(self):
        """Test suspicious_transactions property returns correct data."""
        handler = OutputHandler(self.account_summaries,
                               self.suspicious_transactions,
                               self.transaction_statistics)
        self.assertEqual(handler.suspicious_transactions, self.suspicious_transactions)

    def test_transaction_statistics_property(self):
        """Test transaction_statistics property returns correct data."""
        handler = OutputHandler(self.account_summaries,
                               self.suspicious_transactions,
                               self.transaction_statistics)
        self.assertEqual(handler.transaction_statistics, self.transaction_statistics)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('csv.writer')
    def test_write_account_summaries_to_csv(self, mock_writer, mock_open):
        """Test writing account summaries to CSV creates correct file."""
        handler = OutputHandler(self.account_summaries,
                               self.suspicious_transactions,
                               self.transaction_statistics)
        handler.write_account_summaries_to_csv("test_accounts.csv")
        
        # Verify file was opened for writing
        mock_open.assert_called_once_with("test_accounts.csv", "w", newline="")
        
        # Verify correct number of rows were written (header + 2 accounts)
        self.assertEqual(mock_writer.return_value.writerow.call_count, 3)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('csv.writer')
    def test_write_suspicious_transactions_to_csv(self, mock_writer, mock_open):
        """Test writing suspicious transactions to CSV creates correct file."""
        handler = OutputHandler(self.account_summaries,
                               self.suspicious_transactions,
                               self.transaction_statistics)
        handler.write_suspicious_transactions_to_csv("test_suspicious.csv")
        
        mock_open.assert_called_once_with("test_suspicious.csv", "w", newline="")
        self.assertEqual(mock_writer.return_value.writerow.call_count, 2)  # header + 1 transaction

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('csv.writer')
    def test_write_transaction_statistics_to_csv(self, mock_writer, mock_open):
        """Test writing transaction statistics to CSV creates correct file."""
        handler = OutputHandler(self.account_summaries,
                               self.suspicious_transactions,
                               self.transaction_statistics)
        handler.write_transaction_statistics_to_csv("test_stats.csv")
        
        mock_open.assert_called_once_with("test_stats.csv", "w", newline="")
        self.assertEqual(mock_writer.return_value.writerow.call_count, 3)  # header + 2 transaction types

if __name__ == "__main__":
    unittest.main()