from datetime import date
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
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

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

# Users Table
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String, default="user")  # "user" or "admin"

    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),)