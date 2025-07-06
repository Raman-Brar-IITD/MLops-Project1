import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

#constants for log configuration
LOG_DIR='logs'
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
Max_LOG_SIZE=5 * 1024 * 1024  # 5 MB
BACKUP_COUNT=3

# Create log directory if it doesn't exist
log_dir_path=os.path.join(from_root(),LOG_DIR)
os.makedirs(log_dir_path,exist_ok=True)
log_file_path=os.path.join(log_dir_path,LOG_FILE)

def configure_logger():
    """Configures logging with a rotating file handler and a console handler"""
    #Creating a Custom logger
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #Define formatter
    formatter=logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    #File handler with rotation
    file_handler=RotatingFileHandler(log_file_path,maxBytes=Max_LOG_SIZE,backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    #console handler
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    #Adding handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logging.getLogger("pymongo").setLevel(logging.WARNING)

#configure the logger
configure_logger()