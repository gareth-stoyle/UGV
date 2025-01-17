import argparse
import sys

from config.config import config
from src.ugv_system import UGVSystem
from src.logger import customLogger
from src.utils import is_raspberry_pi5, run_tests, delete_file, print_ugv_system_banner


def tidy_up():
    logger.info("Tidy up PLACEHOLDER.")
    logger.info("Tidy up complete.")


### Variables ###
log_file = "log/app.log"
# Determine the GPIO Serial Device Name Based on the Raspberry Pi Model
base_path = "/dev/ttyAMA0" if is_raspberry_pi5() else "/dev/serial0"

parser = argparse.ArgumentParser(description="UGV System")
parser.add_argument("--debug", action="store_true", help="output debug to CLI.")
args = parser.parse_args()


### Setup logging ###
delete_file(log_file)
logger = customLogger("main", log_file, args.debug)


### Run tests ###
logger.info("Initiating testing...")

if not run_tests():
    logger.critical("Tests failed! Exiting.")
    tidy_up()
    sys.exit(1)

logger.info("Testing passed, running UGV system!")


### Run system ###
print_ugv_system_banner(logger)
system = UGVSystem(config=config, base_path=base_path, debug_logging=args.debug)
system.run()


### Tidy up ###
tidy_up()
