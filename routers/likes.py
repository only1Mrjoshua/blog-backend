# routers/likes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Like
from schemas import LikeBase, LikeResponse
from auth import get_current_user, get_db

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", response_model=LikeResponse)
def like_post(
    like: LikeBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]

    existing_like = db.query(Like).filter(
        Like.user_id == user_id, Like.post_id == like.post_id
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this post")

    new_like = Like(user_id=user_id, post_id=like.post_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


@router.delete("/{post_id}")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]

    like = db.query(Like).filter(
        Like.user_id == user_id, Like.post_id == post_id
    ).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()
    return {"message": "Unliked successfully"}


@router.get("/count/{post_id}")
def get_like_count(post_id: int, db: Session = Depends(get_db)):
    count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"post_id": post_id, "total_likes": count}

# Add to routers/likes.py

@router.get("/status/{post_id}")
def get_like_status(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Checks if the current authenticated user has liked the given post."""
    user_id = current_user["id"]
    
    existing_like = db.query(Like).filter(
        Like.user_id == user_id, Like.post_id == post_id
    ).first()

    # If a like exists, return true, otherwise false
    return {"post_id": post_id, "is_liked": bool(existing_like)}