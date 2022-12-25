import os 
SECRET_KEY = os.environ.get("APP_SCRET_KEY", 'nopassword')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DB_PORT = os.environ.get("DB_PORT", 3306)
DB_USER = os.environ.get("DB_USER", "root")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "quanlykhachsan")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

HOTEL_IMAGE = os.environ.get("HOTEL_IMAGE", "D:\\hotel_image")

USER_IMAGE = os.environ.get("USER_IMAGE", "D:\\CƠ CỞ WEB\\WEB\\project\\final\\app\\templates\\user")