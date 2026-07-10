from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')

def hash_pwd(plain_pwd:str):
	return pwd_context.hash(plain_pwd)


def verify(plain_password,hashed_password):
	return pwd_context.verify(plain_password,hashed_password)