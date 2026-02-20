from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.like import Like
from app.models.match import Match
from app.models.user import User
from fastapi import HTTPException
import uuid

def like_user(db: Session, liker_id: uuid.UUID, liked_id: uuid.UUID) -> dict:
    # Check if users exist
    liker = db.query(User).filter(User.id == liker_id).first()
    liked = db.query(User).filter(User.id == liked_id).first()
    
    if not liker or not liked:
        raise HTTPException(status_code=404, detail="User not found")
    
    if liker_id == liked_id:
        raise HTTPException(status_code=400, detail="Cannot like yourself")
    
    # Check if already liked
    existing_like = db.query(Like).filter(
        Like.liker_id == liker_id, 
        Like.liked_id == liked_id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked this user")
    
    # Create the like
    like = Like(liker_id=liker_id, liked_id=liked_id)
    
    try:
        db.add(like)
        db.flush()  # Flush to get the like in the DB for match check
        
        # Check if it's a mutual like (match)
        mutual_like = db.query(Like).filter(
            Like.liker_id == liked_id,
            Like.liked_id == liker_id
        ).first()
        
        is_match = False
        if mutual_like:
            # Create a match
            match = Match(user_1=liker_id, user_2=liked_id)
            db.add(match)
            is_match = True
        
        db.commit()
        return {"status": "liked", "is_match": is_match}
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already liked this user")

def get_user_likes(db: Session, user_id: uuid.UUID) -> list:
    likes = db.query(Like).filter(Like.liker_id == user_id).all()
    return [{"liked_id": like.liked_id, "created_at": like.created_at} for like in likes]

def get_user_matches(db: Session, user_id: uuid.UUID) -> list:
    matches = db.query(Match).filter(
        (Match.user_1 == user_id) | (Match.user_2 == user_id)
    ).all()
    
    match_list = []
    for match in matches:
        other_user_id = match.user_2 if match.user_1 == user_id else match.user_1
        match_list.append({
            "match_id": match.id,
            "other_user_id": other_user_id,
            "created_at": match.created_at
        })
    
    return match_list