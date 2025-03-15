import configparser
import os
import sys
from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = os.path.dirname(sys.path[0])
config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, "data/config.ini"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if OPENAI_API_KEY == None or os.getenv('OPENAI_API_KEY') == None:
    raise ValueError("You do not have a API key set")