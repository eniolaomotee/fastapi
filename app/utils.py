from passlib.context import CryptContext

# Telling Passlib which hashing algorithm we want to use which is Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)


def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)