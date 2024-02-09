# from fastapi import APIRouter, Depends, status, HTTPException, UploadFile
# from .. import schemas, database, models, oauth2
# from sqlalchemy.orm import Session
# from ..repositories import process_results
# from ..import oauth2
# from typing import List, Union
# import os
# from dotenv import load_dotenv
# from ..hashing import Hash

# load_dotenv()

# router= APIRouter(prefix="/label", tags= ["Label"])
# get_db= database.get_database


# USERNAME= os.getenv('ADMIN_USER')
# ROLE=  'admin'
# EMAIL=  os.getenv('ADMIN_EMAIL')
# try:
#     PASSWORD= Hash.enc(os.getenv('ADMIN_PASSWORD'))
# except:
#     pass

# # , response_model= schemas.ImageResult,
# @router.post('/process-results', status_code= status.HTTP_200_OK) #old_image: UploadFile, 
# async def process_label(new_image: UploadFile, db: Session= Depends(get_db), current_user: schemas.UserLogin= Depends(oauth2.get_current_user)):
#     return await process_results.process_label(new_image, current_user.username, db)

