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