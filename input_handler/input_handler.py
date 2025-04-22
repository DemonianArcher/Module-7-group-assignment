"""
InputHandler Module

This module provides functionality to handle input files in CSV and JSON formats.
It includes methods to read and parse data from these files into a list of transactions.

Classes:
    InputHandler: Handles input file operations such as reading and parsing data.

Author: Avery Cloutier
Version: 1.0
"""

import csv
import json
from os import path

__author__ = "Avery Cloutier"
__version__ = "1.0"


class InputHandler:
    """
    A class to handle input files and parse their data.

    This class supports reading data from CSV and JSON files. It provides methods
    to determine the file format, validate file existence, and parse the data into
    a list of transactions.

    Attributes:
        file_path (str): The path to the input file.
    """

    # Class-level validation rules (example)
    VALIDATION_RULES = {
        'required_keys': {'Transaction ID', 'Account number', 'Date', 'Transaction type', 'Amount', 'Currency', 'Description'},
        'valid_transaction_types': {'deposit', 'withdrawal', 'transfer'}
    }

    def __init__(self, file_path: str):
        """
        Initializes the InputHandler with the specified file path.

        Args:
            file_path (str): The path to the input file.
        """
        self.__file_path = file_path

    @property
    def file_path(self) -> str:
        """
        Gets the file path of the input file.

        Returns:
            str: The file path of the input file.
        """
        return self.__file_path

    def get_file_format(self) -> str:
        """
        Determines the format of the input file based on its extension.

        Returns:
            str: The file format (e.g., 'csv', 'json').
        """
        return self.__file_path.split(".")[-1]

    def read_input_data(self) -> list:
        """
        Reads and parses data from the input file.

        This method determines the file format, calls the appropriate method
        to parse the data, and validates the parsed transactions.

        Returns:
            list: A list of validated transactions parsed from the input file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is unsupported.
        """
        transactions = []
        file_format = self.get_file_format()

        if file_format == "csv":
            transactions = self.read_csv_data()
        elif file_format == "json":
            transactions = self.read_json_data()
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

        # Validate the transactions using the class-level VALIDATION_RULES
        validated_transactions = self.data_validation(transactions, self.VALIDATION_RULES)

        return validated_transactions

    def read_csv_data(self) -> list:
        """
        Reads and parses data from a CSV file.

        Returns:
            list: A list of transactions parsed from the CSV file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")

        transactions = []

        with open(self.__file_path, "r") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                transactions.append(row)

        return transactions

    def read_json_data(self) -> list:
        """
        Reads and parses data from a JSON file.

        Returns:
            list: A list of transactions parsed from the JSON file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")

        with open(self.__file_path, "r") as input_file:
            transactions = json.load(input_file)

        return transactions

    def data_validation(self, transactions: list, validation_rules: dict) -> list:
        """
        Validates the parsed data.

        This method filters out invalid transactions from the provided list. A valid transaction
        is a dictionary that contains all the required keys and satisfies the validation rules
        provided in the `validation_rules` parameter.

        Args:
            transactions (list): A list of dictionaries containing transaction data.
            validation_rules (dict): A dictionary containing validation rules, including:
                - 'required_keys': A set of keys that must be present in each transaction.
                - 'valid_transaction_types': A set of valid transaction types.

        Returns:
            list: A list of dictionaries containing only valid transactions.
        """
        required_keys = validation_rules.get('required_keys', set())
        valid_transaction_types = validation_rules.get('valid_transaction_types', set())

        valid_transactions = []
        for transaction in transactions:
            # Check if the transaction contains all required keys
            if not isinstance(transaction, dict) or not required_keys.issubset(transaction.keys()):
                continue

            # Validate 'Amount' (must be a non-negative numeric value)
            try:
                amount = float(transaction['Amount'])
                if amount < 0:
                    continue
            except (ValueError, TypeError):
                continue

            # Validate 'Transaction type' (must be one of the valid types)
            if transaction['Transaction type'] not in valid_transaction_types:
                continue

            # If all validations pass, add the transaction to the valid list
            valid_transactions.append(transaction)

        return valid_transactions
