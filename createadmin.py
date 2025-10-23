# create_admin.py
from database import SessionLocal  
from models import Users           
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin(username: str, raw_password: str, db):
    hashed = bcrypt_context.hash(raw_password)
    user = Users(username=username, hashed_password=hashed, role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

if __name__ == "__main__":
    db = SessionLocal()
    username = "admin"
    password = "admin12345"
    user = create_admin(username, password, db)
    print("Created admin:", user.id, user.username)
    db.close()