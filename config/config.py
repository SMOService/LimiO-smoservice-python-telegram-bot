import os

creator = 36082701
database_name = 'database.db'
admins = [creator]


api_url = 'https://smoservice.media/api/'
api_key = os.getenv('API_KEY', '')
api_key_secret = os.getenv('API_KEY_SECRET', '')
user_id_secret = 961023
user_id = 189515

email = os.getenv('SMO_EMAIL', '')
password = os.getenv('SMO_PASSWORD', '')
