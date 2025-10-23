from datetime import date
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Annotated, Optional
from sqlalchemy import desc
import auth
from auth import get_current_user
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

# Allow frontend at 127.0.0.1:5500 to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Contact Messages
# ---------------------------
class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessageResponse(ContactMessageBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------
# Newsletter Subscriptions
# ---------------------------
class NewsletterSubscriptionBase(BaseModel):
    email: EmailStr

class NewsletterSubscriptionCreate(NewsletterSubscriptionBase):
    pass

class NewsletterSubscriptionResponse(NewsletterSubscriptionBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------
# Posts
# ---------------------------
class PostBase(BaseModel):
    category: str
    title: str
    image1: Optional[str] = None
    intro_content: Optional[str] = None
    content1: Optional[str] = None
    quote: Optional[str] = None
    quote_author: Optional[str] = None
    main_content: Optional[str] = None
    image2: Optional[str] = None
    final_content: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: date

    class Config:
        from_attributes = True


# ---------------------------
# Traffic
# ---------------------------
class TrafficBase(BaseModel):
    visit_date: date
    visit_count: int = 1

class TrafficCreate(TrafficBase):
    pass

class TrafficResponse(TrafficBase):
    id: int

    class Config:
        from_attributes = True



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/contact/", status_code=status.HTTP_200_OK)
async def read_contact_messages(db: db_dependency):
    messages = db.query(models.ContactMessage).all()
    return messages

@app.post("/contact/", status_code=status.HTTP_201_CREATED)
async def create_contact_message(message: ContactMessageCreate, db: db_dependency):
    db_message = models.ContactMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.post("/subscribe/", status_code=status.HTTP_201_CREATED)
async def create_newsletter_subscription(subscription: NewsletterSubscriptionCreate, db: db_dependency):
    db_subscription = models.NewsletterSubscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@app.get("/subscribe/", status_code=status.HTTP_200_OK)
async def read_newsletter_subscriptions(db: db_dependency):
    subscriptions = db.query(models.NewsletterSubscription).all()
    return subscriptions

@app.post("/posts/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(
        **post.dict(),
        created_at=date.today()  # 👈 always today's date
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts/", status_code=status.HTTP_200_OK)
async def read_posts(db: db_dependency):
    posts = db.query(models.Post).all()
    return posts

@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post: PostBase, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/recent")
def get_recent_posts(db: Session = Depends(get_db)):
    posts = (
        db.query(models.Post)
        .order_by(desc(models.Post.created_at))
        .limit(6)
        .all()
    )
    return posts

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return db_post

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"User": user}
