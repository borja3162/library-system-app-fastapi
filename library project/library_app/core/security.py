from datetime import datetime, timedelta ,timezone
from jose import jwt
from passlib.context import CryptContext

from library_app.core.env_settings import EnvSettings





pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto", # marks any scheme not in schemes' list as deprecated
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)







settings = EnvSettings()



def create_access_token(data: dict, minutes_to_expire: int | None = None):
    to_encode = data.copy()

    minutes = minutes_to_expire if minutes_to_expire is not None else  settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.DATA_VALIDATION_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, settings.DATA_VALIDATION_KEY, algorithms=[settings.ALGORITHM])