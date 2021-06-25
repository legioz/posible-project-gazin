from dotenv import load_dotenv
import os

load_dotenv()

config = os.environ

SECRET_KEY = config.get('SECRET_KEY', None)
PROJECT_NAME = config.get('PROJECT_NAME', None)
DEBUG = config.get('DEBUG', None)
