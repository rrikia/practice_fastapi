from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from typing import Optional, List

# We need the app from main.py 
# Create a router object
router = APIRouter(
    prefix="/posts",
    tags=["Posts"])


# Get all posts
# FastAPI will automatically serialize my_posts to a JSON
# Response model: respond a list of Posts
# /posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user : int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # Code to get all posts using raw SQL
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # print(limit)
    # return a list of posts 
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # by default in SQLAlchemy join, it's a left inner join
    # but here we want a left outer join 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
          models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # From fixing bug, no idea 
    results = list(map(lambda x: x._mapping, results))

    return results

# Create (save) posts
# Save the posts into a database
# /posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):
    # SQL query
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """
    #               , (post.title, post.content, post.published))
    # Return the newly created post
    # new_post = cursor.fetchone()
    # Commit change back to database
    # conn.commit()

    # Unpack Pydantic schema dictionary into SQLAlchemy Model
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) 
    db.add(new_post)
    # Commit the change to the database
    db.commit()
    db.refresh(new_post) # Pull new values back from DB (like generated ID)
    return new_post


# get 1 post by id
# id field is a path parameter
# /posts/{id}
@router.get("/{id}", response_model=schemas.PostOut)
# Every path parameter is returned as a string so convert it into int
def get_post(id: int, db: Session = Depends(get_db),
             current_user : int = Depends(oauth2.get_current_user)):
    # id must be a str in the SQL query
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)),)
    # post = cursor.fetchone()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
          models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return post
    

# Delete a post
# /posts/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):
    # empty comma is to avoid any potential issue
    # no idea why
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)),)
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # Define the query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # cannot find the post to delete 
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    # current user id is != the post's owner id
    if post.owner_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    # Find the original query anf append the delete to it 
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# Update a post
# Follow the schema of pydantic model
# /posts/{id}
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", 
    #               (post.title, post.content, post.published, (str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # Query to find the post with the id 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    # If the post exists

    # current user id is != the post's owner id
    if post.owner_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    # Chain the update method to the same query object
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()