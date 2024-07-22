from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


class Config:
    SECRET_KEY = "your_secret_key"
    JWT_SECRET_KEY = "your_jwt_secret_key"


limiter = Limiter(
    key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]
)
