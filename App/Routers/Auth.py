from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, Schemas, Models, Utility, oauth2

router = APIRouter(tags=['Authentication'])



@router.post('/login', response_model=Schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(database.get_db)):

    user = db.query(Models.User).filter(Models.User.email == user_creds.username).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    if not Utility.validation(user_creds.password, user.password):

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    # print("access_token:", access_token)
    return {"access_token": access_token, "token_type":"bearer"}