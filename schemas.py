from pydantic import BaseModel
from datetime import datetime

# ---------------------- COMMENTS ----------------------
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int


class CommentResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------- LIKES ----------------------
class LikeBase(BaseModel):
    post_id: int


class LikeResponse(LikeBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True