import configparser
import os
import sys
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(sys.path[0])

def make_bool(variable : str) -> bool:
    """
    Turns a string bool into a proper bool + validation
    """
    return variable.strip().lower() == "true"

def check_directory(src_dirname="src"):
    """
    Checks if the directory this is running from is the one above the src directory.
    """
    script_location = os.path.abspath(__file__)
    execution_directory = os.getcwd()
    
    # Gets the the double dirname of the script location and if it is not the execution directory well, bye
    if os.path.dirname(os.path.dirname(script_location)) != execution_directory:
        raise ValueError(f"Please be in the parent directory of src.")

check_directory()
config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, "data/config.ini"))

# Making sure their is a API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY == None or os.getenv('OPENAI_API_KEY') == None:
    raise ValueError("You do not have a API key set")

PROVIDER = config['PROVIDERS']['provider']
OPENAI_MODEL = config['PROVIDERS']['openai_model']

MAX_CHARACTERS = int(config['PREFERENCES']['max_characters'])
