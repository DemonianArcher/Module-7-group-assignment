"""REQUIRED MODULE DOCUMENTATION"""

import logging
from datetime import datetime
from os import path
from input_handler.input_handler import InputHandler
from data_processor.data_processor import DataProcessor
from output_handler.output_handler import OutputHandler

__author__ = "Muhammad Rahmani"
__version__ = "24-April-2025"

def setup_logging(team_number: int) -> logging.Logger:
    """Enables us to log for the application

    Args:
        team_number: The team number for log file naming

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Creates a log file name with team number
    log_filename = f"fdp_team_{team_number}.log"
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # File handler for logging to file
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Console handler for logging to terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def main() -> None:
    """Main function to read input data, process it, and write the 
    results to output files.

    - Reads input data from a CSV file using InputHandler.
    - Processes the data using DataProcessor.
    - Writes the processed data to CSV and JSON files using 
    OutputHandler.
    - Handles any errors with appropriate logging
    """
    # Setting team number
    TEAM_NUMBER = 5

    logger = setup_logging(TEAM_NUMBER)
    logger.info("Starting financial data processing system")

    try:
        # Retrieves the directory name of the current script or module file.
        current_directory = path.dirname(path.abspath(__file__))

        # Joins the current directory, the relative path to the input folder 
        # and the filename to create a complete path to the file.
        input_file_path = path.join(current_directory, "input/input_data.csv")

        logger.info(f"Reading input data from: {input_file_path}")
        input_handler = InputHandler(input_file_path)
        transactions = input_handler.read_input_data()
        logger.info(f"Successfully read {len(transactions)} transactions")

        # Process data with logging
        logger.info("Initializing DataProcessor with INFO level logging")

        data_processor = DataProcessor(
            transactions,
            logging_level = "INFO",
            logging_format = "%(asctime)s - %(levelname)s - %(message)s",
            log_file = f"fdp_team_{TEAM_NUMBER}.log"
        )

        logger.info("Processing transaction data")
        processed_data = data_processor.process_data()
        logger.info("Data processing completed successfully")

        account_summaries = processed_data["account_summaries"]
        suspicious_transactions = processed_data["suspicious_transactions"]
        transaction_statistics = processed_data["transaction_statistics"]
        
        logger.info(f"Processed {len(account_summaries)} accounts")
        logger.info(f"Found {len(suspicious_transactions)} suspicious transactions")
        
        logger.info("Initializing OutputHandler")
        output_handler = OutputHandler(account_summaries, 
                                    suspicious_transactions, 
                                    transaction_statistics)

        # Joins the current directory, the relative path to the output 
        # folder and the filename to create a complete path to each of the 
        # output files.
        file_prefix = "output_data"
        filenames = ["account_summaries", 
                    "suspicious_transactions", 
                    "transaction_statistics"]
        

        file_path = {}

        for filename in filenames:
            file_path[filename] = path.join(current_directory,
                                            f"output/{file_prefix}_{filename}.csv")

        logger.info("Writing output files")
        output_handler.write_account_summaries_to_csv(file_path["account_summaries"])
        output_handler.write_suspicious_transactions_to_csv(file_path["suspicious_transactions"])
        output_handler.write_transaction_statistics_to_csv(file_path["transaction_statistics"])

        logger.info(f"Output files written to: {file_path}")
        logger.info("Financial data processing completed successfully")

    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occured: {e}", exc_info=True)
    finally:
        logging.shutdown()


if __name__ == "__main__":
    main()
