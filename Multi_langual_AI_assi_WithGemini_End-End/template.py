import os 
from pathlib import Path 
import logging 

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# list all the file wnated to create in the project 
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "requirements.txt",
    "Setup.py",
    "app.py",
    "research/trials.py",
    ".gitignore" 
]

# code to create the files 

for filepath in list_of_files:
    file_path = Path(filepath) # create a path object 
    file_dir, file_name = os.path.split(file_path) # split the path into directory and file name 

    # check if the directory or the file already exist in the loacation 
    if file_dir !="":
        os.makedirs(file_dir,exist_ok=True) # create the directory if it does not exist
        logging.info(f"Created a directory at: {file_dir} for the file: {file_name}")

    if (not os.path.exists(filepath)) or (os.path.getsize(str(filepath))==0):
        with open(file_path,"w") as f:
            pass # create the file if it does not exist
            logging.info(f"Created a file at: {file_path}")
    else:
        logging.info(f"The file {file_name} already exists at: {file_path}")

