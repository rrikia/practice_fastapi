from passlib.context import CryptContext


# Keep all the logic related to bcrypt password in this file

# Uses bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# Function to verify that the password is equal
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)