from datetime import datetime
import logging
import os

LOGS_PATH = "./logs/"


def setup_logger(process_id:str,logger_level: int = logging.INFO) -> None:
    """
    Sets up the root logger that logs to a file named with the current date.
    
    Args:
        logger_level (int): Logging level to apply to the logger and all handlers (default: INFO).
    """
    # Ensure the logs directory exists
    os.makedirs(LOGS_PATH, exist_ok=True)

    # Store using process id
    log_filename = os.path.join(LOGS_PATH, f"{process_id}.log")

    # Configure the root logger
    root_logger = logging.getLogger()
    
    # Clear any existing handlers to avoid duplication
    if root_logger.handlers:
        root_logger.handlers.clear()
        
    # Set the logger level
    root_logger.setLevel(logger_level)

    # File handler with the same logging level
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logger_level)

    # Console handler with the same logging level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)

    # Formatter with timestamp, level, and module name prefix
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: %(message)s')

    # Apply formatter to both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)