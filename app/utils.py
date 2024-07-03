from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def verifyLogin(attempt_pwd, hashed_pwd):
    return pwd_context.verify(attempt_pwd, hashed_pwd)