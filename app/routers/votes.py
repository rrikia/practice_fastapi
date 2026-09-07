from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

# Set up a router
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db)
         , current_user: int = Depends(oauth2.get_current_user)):

    # 1. Check if the post even exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {vote.post_id} does not exist"
        )

    # find the vote based on post_id and user_id
    # 2. Query to check if the user has already voted on this post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
        models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    # like a post => dir = 1 => create a new vote
    # unlike a post => dir = 0 => delete an existing vote

    # Add a new vote
    # if found_vote is found, so the post is already liked
    # and the vote.dir == 1, so the post is liked again
    # raise exception 
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        else:
            # It's a new vote because the post is liked by the user 
            # for the first time
            new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}

    # dir == 0, delete a vote
    else:
        if not found_vote:
            # Cannot delete a vote that doesn't exist 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}