import os
import pyfiglet
import subprocess
from typing import Any, Union
import logging

# General util functions

def is_raspberry_pi5() -> bool:
    """Function for Detecting Raspberry Pi version.

    Returns:
        bool: True if the system is Raspberry Pi 5, False otherwise.
    """
    with open("/proc/cpuinfo", "r") as file:
        for line in file:
            if "Model" in line:
                return "Raspberry Pi 5" in line
    return False

def normalise_to_range(
    value: Union[int, float],
    old_min: Union[int, float],
    old_max: Union[int, float],
    new_min: Union[int, float],
    new_max: Union[int, float]
) -> float:
    """Normalise a value from one range to another.

    Args:
        value: The value to normalise.
        old_min: Minimum of the original range.
        old_max: Maximum of the original range.
        new_min: Minimum of the new range.
        new_max: Maximum of the new range.

    Returns:
        float: Normalised value in the new range.

    Raises:
        ValueError: If the old or new range is zero.
    """
    if old_max == old_min:
        raise ValueError("Old range cannot be zero (old_min == old_max).")
    if new_max == new_min:
        raise ValueError("New range cannot be zero (new_min == new_max).")

    return new_min + ((value - old_min) * (new_max - new_min)) / (old_max - old_min)

def run_tests() -> bool:
    """Run pytest tests.

    Returns:
        bool: True if tests pass, False otherwise.
    """
    result = subprocess.run(
        ["pytest", "tests"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.returncode == 0

def delete_file(file_path: str) -> None:
    """Deletes the specified file if it exists.

    Args:
        file_path: Path to the file to delete.
    """
    if os.path.exists(file_path):
        os.remove(file_path)

def print_ugv_system_banner(logger: logging.Logger) -> None:
    """Prints a large 'UGV System' ASCII art banner.

    Args:
        logger: Logger instance to log the banner output.
    """
    banner: str = pyfiglet.figlet_format("UGV System")
    logger.info("Starting System...\n" + banner)
