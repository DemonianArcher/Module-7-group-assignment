"""Module for handling output operations including writing transaction data to CSV files.

This module provides functionality to export processed transaction data in various formats,
including account summaries, suspicious transactions, and transaction statistics.
"""

import csv
import os
from typing import List, Dict

__author__ = "Sharef"
__version__ = "1.0"

class OutputHandler:
    """Handles the output operations for processed transaction data.

    This class provides methods to write different types of transaction data to CSV files,
    including account summaries, suspicious transactions, and transaction statistics.

    Attributes:
        account_summaries (dict): Dictionary containing account summary data.
        suspicious_transactions (list): List of suspicious transactions.
        transaction_statistics (dict): Dictionary containing transaction statistics.
    """

    def __init__(self, account_summaries: dict, 
                       suspicious_transactions: list, 
                       transaction_statistics: dict):
        """Initializes the OutputHandler with processed transaction data.

        Args:
            account_summaries: Dictionary of account summaries where keys are account numbers
                and values are dictionaries containing balance and transaction totals.
            suspicious_transactions: List of transactions flagged as suspicious.
            transaction_statistics: Dictionary of transaction statistics where keys are
                transaction types and values are dictionaries with total amounts and counts.
        """
        self.__account_summaries = account_summaries
        self.__suspicious_transactions = suspicious_transactions
        self.__transaction_statistics = transaction_statistics
    
    @property
    def account_summaries(self) -> dict:
        """dict: Gets the dictionary of account summaries."""
        return self.__account_summaries
    
    @property
    def suspicious_transactions(self) -> list:
        """list: Gets the list of suspicious transactions."""
        return self.__suspicious_transactions
    
    @property
    def transaction_statistics(self) -> dict:
        """dict: Gets the dictionary of transaction statistics."""
        return self.__transaction_statistics

    def write_account_summaries_to_csv(self, file_path: str) -> None:
        """Writes account summary data to a CSV file.

        The output file will contain columns for account number, balance,
        total deposits, and total withdrawals.

        Args:
            file_path: Path to the output CSV file.
        """
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["Account number", 
                           "Balance", 
                           "Total Deposits", 
                           "Total Withdrawals"])

            for account_number, summary in self.__account_summaries.items():
                writer.writerow([account_number,
                               summary["balance"],
                               summary["total_deposits"],
                               summary["total_withdrawals"]])

    def write_suspicious_transactions_to_csv(self, file_path: str) -> None:
        """Writes suspicious transactions to a CSV file.

        The output file will contain all fields from the original transaction data.

        Args:
            file_path: Path to the output CSV file.
        """
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["Transaction ID", 
                           "Account number", 
                           "Date", 
                           "Transaction type", 
                           "Amount", 
                           "Currency", 
                           "Description"])

            for transaction in self.__suspicious_transactions:
                writer.writerow([transaction["Transaction ID"],
                               transaction["Account number"],
                               transaction["Date"],
                               transaction["Transaction type"],
                               transaction["Amount"],
                               transaction["Currency"],
                               transaction["Description"]])

    def write_transaction_statistics_to_csv(self, file_path: str) -> None:
        """Writes transaction statistics to a CSV file.

        The output file will contain transaction type, total amount,
        and transaction count.

        Args:
            file_path: Path to the output CSV file.
        """
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["Transaction type", 
                           "Total amount", 
                           "Transaction count"])

            for transaction_type, statistic in self.__transaction_statistics.items():
                writer.writerow([transaction_type, 
                               statistic["total_amount"], 
                               statistic["transaction_count"]])
    
    def filter_account_summaries(self, filter_field: str, filter_value: int, filter_mode: bool) -> list:
        """Filters account summaries based on specified criteria.

        Args:
            filter_field: Field to filter on ("balance", "total_deposits", or "total_withdrawals")
            filter_value: Value to compare against
            filter_mode: If True, filter for values >= filter_value; if False, filter for values <= filter_value
        
        Returns:
            List of dictionaries containing filtered account summaries
        
        Raises:
            ValueError: If filter_field is not one of the valid options
        """
        
        valid_fields = ["balance", "total_deposits", "total_withdrawals"]
        if filter_field not in valid_fields:
            raise ValueError(f"Invalid filter field. Must be one of: {valid_fields}")
        
        filtered = []
        for account in self.__account_summaries.values():
            account_value = account[filter_field]

            if filter_mode and account_value >= filter_value:
                filtered.append(account)
            elif not filter_mode and account_value <= filter_value:
                filtered.append(account)
        
        return filtered
    
    def write_filtered_summaries_to_csv(self, filtered_data: list, file_path: str) -> None:
        """Writes filtered account summaries to a CSV file.

        Args:
            filtered_data: List of filtered account summaries
            file_path: Path to the output CSV file
        """
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["Account number", 
                            "Balance", 
                            "Total Deposits", 
                            "Total Withdrawals"])
            
            for account in filtered_data:  
                writer.writerow([account["account_number"],
                                account["balance"],
                                account["total_deposits"],
                                account["total_withdrawals"]])