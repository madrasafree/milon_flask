import os

# Database configuration
class ProdConfig:
    API_TOKEN = os.environ.get('MADRASA_SERVER_KEY_SECRET_PROD')

class DevConfig:
    API_TOKEN = os.environ.get('MADRASA_SERVER_KEY_SECRET_DEV')

class TestConfig:
    API_TOKEN = os.environ.get('MADRASA_SERVER_KEY_SECRET_TEST')

config = {
    'DEV': DevConfig,
    'TEST': TestConfig,
    'PROD': ProdConfig
}