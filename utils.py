from passlib.context import CryptContext

# This creates an instance of the CryptContext class, specifying that the bcrypt hashing algorithm should be used
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_pass(password: str):
    """
    takes a plain-text password as input and returns the hashed password as a string
    """
    return pwd_context.hash(password)

def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)

