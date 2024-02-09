from fastapi import APIRouter, Depends, status, HTTPException, UploadFile
from .. import schemas, database, oauth2, models
from sqlalchemy.orm import Session
from ..repositories import user
from . import authentication
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

router= APIRouter(prefix="/user", tags= ["User"])
get_db= database.get_database



@router.get('/manual_verify_user',status_code= status.HTTP_200_OK)
def manual_verify(db: Session= Depends(get_db), current_user: schemas.UserLogin= Depends(oauth2.get_current_user)):
    if db.query(models.Users).filter(models.Users.username == current_user.username).first() == None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)
    print(current_user)


@router.post('/register', status_code= status.HTTP_201_CREATED)
async def user_sign_up(request: schemas.SignUp, db: Session= Depends(get_db)):
    return await user.user_sign_up(request, db)


@router.get('/dashboard', status_code=status.HTTP_200_OK, response_model= schemas.Users)
async def dashboard(db: Session= Depends(get_db), current_user: schemas.UserLogin= Depends(oauth2.get_current_user)):
    return await user.dashboard(db, current_user.username)

@router.post('/scan-label-image', status_code= status.HTTP_201_CREATED)
async def scan_label_image(file_image: UploadFile, db: Session= Depends(get_db), current_user: schemas.UserLogin= Depends(oauth2.get_current_user)):
    return await user.scan_label_image(file_image, current_user.username, db)

@router.post('/add-label-image', status_code= status.HTTP_201_CREATED)
async def add_label_image(file_image: UploadFile, request: schemas.AddLabelImage= Depends(), db: Session= Depends(get_db), current_user: schemas.UserLogin= Depends(oauth2.get_current_user)):
    return await user.add_label_image(request, file_image, current_user.username, db)


@router.post('/update-label-image', status_code= status.HTTP_201_CREATED)
async def update_label_image(file_image: UploadFile, request: schemas.UpdateLabelImage= Depends(), db: Session= Depends(get_db), current_user: schemas.UserLogin= Depends(oauth2.get_current_user)):
    return await user.update_label_image(request, file_image, current_user.username, db)

# @router.post('/replace-label-image', status_code= status.HTTP_201_CREATED)
# async def replace_label_image(file_image: UploadFile, request: schemas.ReplaceLabelImage= Depends(), db: Session= Depends(get_db), current_user: schemas.UserLogin= Depends(oauth2.get_current_user)):
#     return await user.replace_label_image(request, file_image, current_user.username, db)