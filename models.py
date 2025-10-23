from datetime import date
from sqlalchemy import Column, Date, Enum, Integer, String, Text
from database import Base

# Contact Messages Table
class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)


# Newsletter Subscriptions Table
class NewsletterSubscription(Base):
    __tablename__ = "newsletter_subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(255), nullable=False, unique=True)


# Posts Table
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    category = Column(String(100), nullable=False)
    created_at = Column(Date, default=date.today)
    title = Column(String(255), nullable=False)
    image1 = Column(String(255), nullable=True)
    intro_content = Column(Text, nullable=True)
    content1 = Column(Text, nullable=True)
    quote = Column(Text, nullable=True)
    quote_author = Column(String(100), nullable=True)
    main_content = Column(Text, nullable=True)
    image2 = Column(String(255), nullable=True)
    final_content = Column(Text, nullable=True)


# Users Table
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String, default="user")  # "user" or "admin"