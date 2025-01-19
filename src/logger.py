import logging
import random
from termcolor import colored


class customLogger:
    def __new__(cls, name: str, log_file: str, debug: bool) -> logging.Logger:
        """
        Create a custom logger with both console and file handlers.

        Args:
            cls: The class being instantiated.
            name: Name for the logger.
            log_file: Path to the log file.
            debug: Whether to enable debug-level logging.

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
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Pick a random color from the COLOURS list for console output
        colour: str = random.choice(
            ["red", "green", "yellow", "blue", "magenta", "cyan"]
        )

        # Create a custom formatter with color
        class ColouredFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                log_message = super().format(record)
                colored_message = colored(log_message, colour)
                return colored_message

        # Configure console handler formatter with color
        colored_formatter = ColouredFormatter(
            "{asctime} - {name} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(colored_formatter)
        console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        return logger
