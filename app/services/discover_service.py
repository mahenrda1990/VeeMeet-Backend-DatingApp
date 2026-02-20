from sqlalchemy.orm import Session
from app.models.discover import DiscoverBatch, DiscoverCandidate
from app.models.user import User
from app.models.like import Like
from datetime import date
import uuid

def generate_discover_batch(db: Session, user_id: uuid.UUID, target_date: date = None) -> DiscoverBatch:
    if not target_date:
        target_date = date.today()
    
    # Check if batch already exists for this date
    existing_batch = db.query(DiscoverBatch).filter(
        DiscoverBatch.user_id == user_id,
        DiscoverBatch.generated_for == target_date
    ).first()
    
    if existing_batch:
        return existing_batch
    
    # Create new batch
    batch = DiscoverBatch(
        user_id=user_id,
        generated_for=target_date
    )
    db.add(batch)
    db.flush()
    
    # Get users that haven't been liked by this user
    liked_user_ids = db.query(Like.liked_id).filter(Like.liker_id == user_id).subquery()
    
    candidates = db.query(User).filter(
        User.id != user_id,  # Not the current user
        ~User.id.in_(liked_user_ids)  # Not already liked
    ).limit(20).all()  # Limit to 20 candidates per batch
    
    # Add candidates to batch
    for i, candidate in enumerate(candidates):
        discover_candidate = DiscoverCandidate(
            batch_id=batch.id,
            candidate_user_id=candidate.id,
            rank=i + 1,
            reason="Daily curation"
        )
        db.add(discover_candidate)
    
    db.commit()
    db.refresh(batch)
    return batch

def get_discover_candidates(db: Session, user_id: uuid.UUID, target_date: date = None) -> list:
    if not target_date:
        target_date = date.today()
    
    # Get or create batch for this date
    batch = generate_discover_batch(db, user_id, target_date)
    
    # Get candidates with user details
    candidates = db.query(DiscoverCandidate, User).join(
        User, DiscoverCandidate.candidate_user_id == User.id
    ).filter(
        DiscoverCandidate.batch_id == batch.id
    ).order_by(DiscoverCandidate.rank).all()
    
    result = []
    for candidate, user in candidates:
        result.append({
            "user_id": user.id,
            "first_name": user.first_name,
            "gender": user.gender,
            "rank": candidate.rank,
            "reason": candidate.reason
        })
    
    return result