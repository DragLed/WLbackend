from authx import AuthX, AuthXConfig
from database import credentials


config = AuthXConfig()
config.JWT_SECRET_KEY = credentials["JWT_SECRET_KEY"]
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False


security = AuthX(config=config)