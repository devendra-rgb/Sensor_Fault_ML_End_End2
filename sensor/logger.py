import logging
import os
from datetime import datetime

#making the directory for the logs
log_file_dir=os.path.join(os.getcwd(),"logs")

os.makedirs(log_file_dir,exist_ok=True)

#making the logfile name 
log_file_name = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"

log_file_path=os.path.join(log_file_dir, log_file_name)


logging.basicConfig(
    
    filename=log_file_path,
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(filename)s - %(levelname)s - %(message)s"
)