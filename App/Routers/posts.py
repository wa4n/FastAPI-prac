from sqlalchemy import func
from typing import Optional, List
from unittest import result
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import Models, Schemas, Utility, oauth2
from ..Models import Post
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model= List[Schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = []
    # cursor.execute("""SELECT * FROM posts""")
    # posts_query = db.query(Models.Post).filter(
        # Models.Post.owner_id == current_user.id, 
        # Models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(Models.Post, func.count(Models.Votes.post_id).label("Votes")).join(
        Models.Votes, 
        Models.Votes.post_id ==  Models.Post.id, 
        isouter=True
        ).group_by(Models.Post.id).filter(
            Models.Post.title.contains(search)
            ).limit(limit).offset(skip).all()
    
    
    
    # posts = cursor.fetchall()
    
    return posts

@router.get("/{id}", response_model=Schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id =%s""", (id,))
    # post = cursor.fetchone()
    post =db.query(Models.Post, func.count(Models.Votes.post_id).label("Votes")).join(
        Models.Votes, 
        Models.Votes.post_id ==  Models.Post.id, 
        isouter=True
        ).group_by(
            Models.Post.id
        ).filter(
            Models.Post.id == id
        ).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id},  was not found")

    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.PostResponse)
def create_posts(post: Schemas.PostCreate, db: Session = Depends(get_db), current_user: int=
                 Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO posts (title ,content, published ) 
    #                VALUES(%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = Models.Post(
        owner_id = current_user.id,
        **post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int= Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(Models.Post).filter(Models.Post.id == id)
    post = post_query.first()
    # post = get_post

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= f'Post with id: {id} does not exist')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to preform delete")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= Schemas.PostResponse)
def update_posts(id: int, post: Schemas.PostUpdate, db: Session = Depends(get_db), 
                 current_id: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title= %s ,content= %s , published= %s  
    #                WHERE id =%s RETURNING * """, 
    #                (post.title, post.content, post.published,id,))
    
    # updated_posts = cursor.fetchone()
    # conn.commit()
    post_query = db.query(Models.Post).filter(Models.Post.id == id)
    post_1 = post_query.first()
    

    if not post_1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} does not exist')
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_1