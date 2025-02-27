from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from ..database import get_db
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session= Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {vote.post_id} is not found')
    vote_query= db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, 
                                             models.Vote.user_id==current_user.id)
    found_vote= vote_query.first()
    if vote.dir:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'User {current_user.id} has already voted for post {vote.post_id}')
        new_vote= models.Vote(post_id= vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Voted successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No vote found for post {vote.post_id} by user {current_user.id}')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}