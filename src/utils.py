import os
import pyfiglet
import subprocess

# General util functions

def is_raspberry_pi5():
    """Function for Detecting Raspberry Pi version."""
    with open('/proc/cpuinfo', 'r') as file:
        for line in file:
            if 'Model' in line:
                if 'Raspberry Pi 5' in line:
                    return True
                else:
                    return False

def normalise_to_range(value, old_min, old_max, new_min, new_max):
    """Normalise a value from one range to another"""
    return new_min + ((value - old_min) * (new_max - new_min)) / (old_max - old_min)

def run_tests():
    """Run pytest tests"""
    result = subprocess.run(['pytest', 'tests'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def delete_file(file_path):
    """Deletes the specified file if it exists."""
    # Check if the file exists
    if os.path.exists(file_path):
        os.remove(file_path)

def print_ugv_system_banner(logger):
    """Prints a large 'UGV System' ASCII art banner."""
    # Generate ASCII art for 'UGV System'
    banner = pyfiglet.figlet_format("UGV System")
    logger.info("Starting System...\n" + banner)