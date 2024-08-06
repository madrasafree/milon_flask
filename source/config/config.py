from dotenv import load_dotenv
import os

# Database configuration
class ProdConfig:
    API_TOKEN = os.environ.get('MADRASA_SERVER_KEY_SECRET_PROD')

class DevConfig:
    API_TOKEN = os.environ.get('MADRASA_SERVER_KEY_SECRET_DEV')

class TestConfig:
    API_TOKEN = os.environ.get('MADRASA_SERVER_KEY_SECRET_TEST')

env_config = {
    'DEV': DevConfig,
    'TEST': TestConfig,
    'PROD': ProdConfig
}

# DEVELOPMENT SERVER CONFIGURATION:
load_dotenv()
user_name = "postgres"
password = env_config["DEV"].API_TOKEN   # DEVELOPER MUST ADD PASSWORD TO ENVIRONMENT VARIABLE UNDER "MADRASA_SERVER_KEY_SECRET_DEV"
# host_address = "arabic-words-db-server.c5cx9bfmz05i.us-east-1.rds.amazonaws.com"  # REMOTE PRODUCTION
# host_address = "localhost"                                                        # LOCAL DEVELOPMENT
host_address = "0.0.0.0" # LOCAL DEVELOPMENT
db_address = "db"
port_db = "5432"
port_app = "5431"
#mdb = "arabic_words_db"
maintenance_database = "postgres"
db_base_connection_string = f"postgresql://{user_name}:{password}@{db_address}:{port_db}"