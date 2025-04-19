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

        This method determines the file format and calls the appropriate method
        to parse the data.

        Returns:
            list: A list of transactions parsed from the input file.

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

        return transactions

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
