from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "Mayorm. nublado 14°C"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
