import logging
import os
from src.utils import TIME

LOG_FILE = f"{TIME}.log"

log_path = os.path.join(os.getcwd(),"logs")
os.makedirs(log_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    level = logging.INFO,
    format = "[ %(asctime)s ] - %(filename)s - %(lineno)d - %(levelname)s - %(message)s"
)