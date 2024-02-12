from passlib.context import CryptContext


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class hash():
    def bcrypt(password: str):
        return pwd.hash(password)
    
    def verify(hased_passwoerd, plain_password):
        return pwd.verify(plain_password, hased_passwoerd)