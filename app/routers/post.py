from fastapi import FastAPI,Depends,status,HTTPException,Response,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func

# Using APIROUTER and calling an instance of it
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# @router.get("/")
# def root():
#     return {"message": "Welcome to Fast API"}


# Get all the posts
# We use limit to get the number of results we want to show.
# we as well use skip and offset to skip over results as well.
# We can search based on keywords using the search functionality
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int = 10,skip: int = 0,search: Optional[str] = ""):
    
    # print(search)
    # posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    
    
    # so We're trying to write our left join query that is we joined the post and the votes table by the common column which was posts.id so we can then get the number of votes for each post
    # SELECT posts.*,COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id=votes.post_id WHERE posts.id=10 group by posts.id;
    # Wee write this with SQL alchemy as this is the raw SQL,
    
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    
    # Use this code if you're trying to view post per user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return posts
    
  
    # Getting all posts with SQL
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"data":posts}

# Using pydantic(Base Model) for our data validation from the user.
# Create Post- retrieve the post and add to the post array,also use to pydantic to validate the post



# So adding the get_current_user is a dependency telling users they need to be authenticated for them to create post, and the get_current_user is basically just calling the verify token and returning the  user_id
# Create Post
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): 
    
    print(current_user.id)
    # When trying to create a post right, it would throw an error because it's trying to access the owner id and we didn't specify it in our schema of PostCreate, but remember we have access to that based on the get_current_user so we'd need to pass it into our dict when creating a post.
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # uvicorn src.main:app --port=5081
    
    # creating Posts with SQL
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published)) 
    
    # new_post = cursor.fetchone()
    
    # conn.commit()
       
       
    # normal Create Post without SQL
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,100000)
    # my_posts.append(post_dict)
    
    return new_post



# Retrieving one single post (Performing validation as well)
# Getting response codes as well as status codes when a resource is been created or gotten from a database.
@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    
    # Get posts via SQL Queries
    # cursor.execute(""" SELECT * FROM posts WHERE id= %s""",(str(id),))
    # post = cursor.fetchone()
    
    # Get post by Id Normal way
    # for post in my_posts:
    #     if post['id'] == id:
    #         return {"post_detail":post}
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")

    # if post.owner_id != current_user:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action")

    return post




# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    # Deleting a post via SQL QUERIES
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    
    # conn.commit()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
    # Check to see if the user who is logged in actually own this post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    # Deleting a post the normal way via the index
    # for index,post in enumerate(my_posts):
    #     if post['id'] == id:
    #         my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update a Post
@router.put("/{id}",response_model=schemas.PostOut)
def update_post(id:int,updated_post:schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post_query = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    
    
    # Extract the post and vote count from the query
    post_with_votes = post_query.first()
    
    if post_with_votes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} does not exist")
    
    # Seperate the post instance and votes count from the query results
    post, votes_count = post_with_votes
    
    
    # Check if the post owner is the current user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    # Update only the 'post' instance 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    
    updated_post_with_votes = post_query.first()
    if updated_post_with_votes:
        post_data,votes_count = updated_post_with_votes
        response_data ={
            "Post": post_data,
            "votes": votes_count
        }
    return response_data
    
    # # Updating post with SQL QUERIES
    # cursor.execute(""" UPDATE posts SET title =%s,content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    
    # conn.commit()
    
    
    # if post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
    # if post.owner_id == current_user.id:
    #     raise HTTPException(detail="Testing")
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorized to perform requested action")
    
    # post.update(updated_post.dict(),synchronize_session=False)
    
    # db.commit()
    
    # Updating Our Post with Normal code with the id 
    # for index,posts in enumerate(my_posts):
    #     if posts['id'] == id:
    #         post_dict = post.dict()
    #         post_dict['id'] = id
    #         my_posts[index]= post_dict 
            
    #         return {"messge":"Post updated successfully", "post":post_dict}
    # return  post_query.first()



# Using an ORM 
# Prevents SQL injection, b. perform db operations without SQL queries with normal python code c. Sits between the database and us
