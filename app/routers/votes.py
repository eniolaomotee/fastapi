from fastapi import HTTPException,Response, status,Depends,FastAPI,APIRouter
from sqlalchemy.orm import Session
from .. import database,schemas,models,oauth2


router = APIRouter(
    tags=["Vote"],
    prefix="/vote"
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session=Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {vote.post_id} does not exist")
    # So in checking our Vote system, we want to check to see for 2 things
    # a. If a vote is 1; if this is the case we want to check if the post has been voted before by the user as well as check if it's the right user that's voting on that post,
    # Remember the way our vote system works a user can vote on multiple posts but can't vote on the same post twice e.g User with id 4 can vote on post with post_id 3 and also vote on post_id 4, but user with id 4 can't vote on post_id 4 cause it would be a duplicate and that is what we're preventing
    
    # So we're checking if the vote.dir is 1 then querying the vote table which contains the post_id and user_id and we're filtering based on if the post_id on the vote table matches the post id we want to vote on, we also check if the user_id is the current user id 
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
     
    found_vote = vote_query.first()
    
    # So from this our logic, above we're querying for the vote and when we get it we want to check if vote_dir is 1 if it's 1 it means the user as already liked it and can't like it again so we throw an error, but it's it's not found we go ahead and create the vote with the post_id been the vote.post_id and the user_id been the current_user.id, we then add then commit it to the db which means hence forth that user has voted that post.
    #  We also check if the direction is 0 which  means the user wants to delete the vote on that post, so we first check if the user has a post he has voted on before, if he doesn't we throw an error, and if he does we go ahead and delete that vote and the user should be good.
    
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on this post {vote.post_id}")
        
        new = models.Vote(post_id= vote.post_id,user_id= current_user.id)
        db.add(new)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted Vote"}
       
  