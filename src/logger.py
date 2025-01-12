import logging

class customLogger:
    def __new__(cls, name, log_file):
        """
        Create a custom logger with both console and file handlers.

        Args:
            name: Name for the logger.

        Returns:
            logger: Configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Create a console handler to output logs to the console
        console_handler = logging.StreamHandler()
        # Create a file handler to save logs to a file
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # Log format for both handlers
        formatter = logging.Formatter(
            "{asctime} - {name} - {levelname} - {message}", 
            style="{", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Configure handlers
        console_handler.setFormatter(formatter)
        console_handler.setLevel("INFO")
        file_handler.setFormatter(formatter)
        file_handler.setLevel("DEBUG")

        return logger

