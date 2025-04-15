"""REQUIRED MODULE DOCUMENTATION"""

import unittest
from unittest import TestCase
from input_handler.input_handler import InputHandler

__author__ = ""
__version__ = ""

class InputHandlerTests(TestCase):
    """Defines the unit tests for the InputHandler class."""

    def setUp(self):
        """This function is invoked before executing a unit test
        function.

        The following class attribute has been provided to reduce the 
        amount of code needed when testing the InputHandler class in 
        the tests that follow.
        
        Example:
            >>> data_processor = DataProcessor(self.FILE_CONTENTS)
        """
        self.FILE_CONTENTS = \
            ("Transaction ID,Account number,Date,Transaction type,"
            + "Amount,Currency,Description\n"
            + "1,1001,2023-03-01,deposit,1000,CAD,Salary\n"
            + "2,1002,2023-03-01,deposit,1500,CAD,Salary\n"
            + "3,1001,2023-03-02,withdrawal,200,CAD,Groceries")

    # Define unit test functions below

if __name__ == "__main__":
    unittest.main()
