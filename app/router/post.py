from fastapi import HTTPException, status, Depends, Response, APIRouter
from typing import List, Optional

from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def posts(db: Session = Depends(get_db), user_id: int= Depends(oauth2.get_current_user), limit: int= 10, skip: int= 0,
          search: Optional[str]= ""):
    """
    Gets all the posts in the DB
    """
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    posts= db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Posts.id, isouter=True).group_by(models.Posts.id).\
        filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    """
    Gets post by given id
    """
    #cursor.execute(""" SELECT * FROM posts WHERE id=%s""", (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Posts.id, isouter=True).group_by(models.Posts.id).\
            filter(models.Posts.id == id).first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} is not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    """
    Creates posts instance based on the BaseModel class
    """
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Posts(owner_id = user_id.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    """
    Deletes a post instance by id
    """
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Given id {id} is not found")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # Return statement not required when 204

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session= Depends(get_db), user_id: int= Depends(oauth2.get_current_user)):
    """
    Updates given fields of the given instance by id
    """
    #cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id=%s RETURNING * """, 
    #               (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    updt_post = post_query.first()
    if updt_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Given id {id} is not found")
    
    if updt_post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()