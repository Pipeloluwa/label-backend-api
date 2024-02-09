from .. import models
from ..hashing import Hash
from ..routers import process_results
from .. image_processing import image_master_process
from .import s3Bucket
from fastapi import HTTPException, status, Response, File
import time
import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

async def process_label(new_image, username, db):
    get_user_id = db.query(models.Users).filter(models.Users.username == username)
    bucket_folder_path = f'users/{get_user_id.first().id}/label_images'

    image_labels= db.query(models.ImageLabels).filter(models.ImageLabels.user_id== get_user_id.first().id).all()
    if image_labels != []:
        for i in image_labels:
            get_image = db.query(models.Images).filter(models.Images.image_label_id== i.id).first()
            if get_image:
                get_image_link= await s3Bucket.s3_get_presigned_link(bucket_folder_path, get_image.image_path)

                # +++++++++++++++++++++++ OCR TESSERACT PROCESS SESSION +++++++++++++++++++++++++
                check_match =  await image_master_process.fetch_image_result(get_image_link, new_image, False)
                # ++++++++++++++++++++++++++++++ END +++++++++++++++++++++++++++++++++

                all_image_details= {"image_details": i, "disparity_details": check_match}


                # ++++++++ SHOULD NO MACTH EXISTS +++++++++++++++++
                if check_match["detail"][result] == False:
                    if not get_user_id.first():
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your account has been removed")

                    if get_user_id.first().role == "student":
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="You are not authorized to view this content")

                    if get_user_id.first().activated == "false":
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Your account was deactivated, please send us mail in the contact centre to access your account")

                    if not get_user_id.first().id:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f"user with this username: '{username}' does not exist or has been removed")


                    bucket_folder_path = f'users/{get_user_id.first().id}/label_images'
                    get_url= await s3Bucket.s3_upload_label(new_image, bucket_folder_path)

                    label_images = models.ImageLabels(label= request.label.lower(), user_id= get_user_id.first().id)
                    db.add(label_images)
                    db.commit()
                    db.refresh(label_images)
                    # get_label_images= db.query(models.ImageLabels).filter(models.ImageLabels.id)
                    images = models.Images(
                        label= request.label.lower(), ingredient= request.ingredient.lower(), image_path= get_url, image_label_id= label_images.id
                    )

                    db.add(label_images)
                    db.add(images)
                    db.commit()
                    db.refresh(label_images)
                    db.refresh(images)
                    break

                # return all_image_details
    else:
        if not get_user_id.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your account has been removed")

        if get_user_id.first().role == "student":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You are not authorized to view this content")

        if get_user_id.first().activated == "false":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Your account was deactivated, please send us mail in the contact centre to access your account")

        if not get_user_id.first().id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"user with this username: '{username}' does not exist or has been removed")


        bucket_folder_path = f'users/{get_user_id.first().id}/label_images'
        get_url= await s3Bucket.s3_upload_label(new_image, bucket_folder_path)

        label_images = models.ImageLabels(label= request.label.lower(), user_id= get_user_id.first().id)
        db.add(label_images)
        db.commit()
        db.refresh(label_images)
        # get_label_images= db.query(models.ImageLabels).filter(models.ImageLabels.id)
        images = models.Images(
            label= request.label.lower(), ingredient= request.ingredient.lower(), image_path= get_url, image_label_id= label_images.id
        )

        db.add(label_images)
        db.add(images)
        db.commit()
        db.refresh(label_images)
        db.refresh(images)          

