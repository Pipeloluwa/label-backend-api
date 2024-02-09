from .. import models, schemas
from ..hashing import Hash
from ..routers import otp_management
from  . import  s3Bucket, file_names_processing

from .. image_processing import image_master_process
from fastapi import HTTPException, status, Response
from PIL import Image, ImageOps
import os
import json
from dotenv import load_dotenv

load_dotenv()



async def user_sign_up(request, db):
    if request.username == os.getenv('ADMIN_USER'):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this username is already taken")
    if db.query(models.Users).filter(models.Users.username == request.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this username is already taken")
    if db.query(models.Users).filter(models.Users.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this email is already taken")

    new_user = models.Users(username=request.username.lower(),
                            email=request.email.lower(),
                            password=Hash.enc(request.password)
                            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def dashboard(db, username):
    get_user_id = db.query(models.Users).filter(models.Users.username == username)

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

    return get_user_id.first()
    # # +++++++ PARSING OBJECTS TO RESTRUCTURE THE RESPONSE MODEL BY SUBSTITUTING A PREFFERED LINK FROM S3 BUCKET FOR THE NAME OF THE FILE STORE IN THE DB
    # query_object = db.query(models.CoursesTags).filter(models.CoursesTags.user_id == get_user_id.first().id).all()
    #
    # # +++++ NOW PARSING THE OBJECT QUERY INSTANCE INTO RESPONSE PYDANTIC MODEL AND SETTING THE PREFERRED LINK INTO IT
    # object_to_json_list = []
    # for i in query_object:
    #     bucket_folder_path = f'user/label_images/{i.id}/cover_picture'
    #     object_to_json = schemas.CoursesTags.parse_obj(
    #         i)  # TP MAKE THIS WORK, YOU WIL HAVE TO SET THE from orm TO TRUE IN THE SCHEMA MODEL CLASS CONFIG, SO THIS WILL THEN BE ABLE TO PARSE IN THE OBJECT
    #
    #     get_preferred_link = await s3Bucket.s3_get_presigned_link(bucket_folder_path, i.cover_picture)
    #     object_to_json.cover_picture = get_preferred_link
    #
    #     for i2 in object_to_json.label_images:
    #         # +++++++ FILE PICTURE +++++++
    #         bucket_folder_path = f'user/label_images/{i.id}/file_picture'
    #         get_preferred_link = await s3Bucket.s3_get_presigned_link(bucket_folder_path, i2.cover_picture)
    #         # print(get_preferred_link)
    #         i2.cover_picture = get_preferred_link
    #         # +++++ VIDEO ++++++
    #         bucket_folder_path = f'user/label_images/{i.id}/file_video'
    #         get_preferred_link = await s3Bucket.s3_get_presigned_link(bucket_folder_path, i2.video)
    #         i2.video = get_preferred_link
    #         # ++++++ PDF +++++++
    #         bucket_folder_path = f'user/label_images/{i.id}/file_pdf'
    #         if i2.pdf:
    #             get_preferred_link = await s3Bucket.s3_get_presigned_link(bucket_folder_path, i2.pdf)
    #             i2.pdf = get_preferred_link
    #
    #     object_to_json_list.append(object_to_json)
    # return object_to_json_list


async def scan_label_image(new_image, username, db):
    all_image_details= None
    
    get_user_id = db.query(models.Users).filter(models.Users.username == username)
    bucket_folder_path = f'users/{get_user_id.first().id}/label_images'

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

    # new_image= await convert_quality(new_image)
    # print(new_image)



    image_labels= db.query(models.ImageLabels).filter(models.ImageLabels.user_id== get_user_id.first().id).all()
    if image_labels != []:
        for i in image_labels:
            get_image = db.query(models.Images).filter(models.Images.label== i.label).first()
            if get_image:
                get_image_link= await s3Bucket.s3_get_presigned_link(bucket_folder_path, get_image.image_path)
                check_match =  await image_master_process.fetch_image_result(get_image_link, new_image.file)
                # print(check_match)
                return check_match['images'][0]
                break
                all_image_details= {"image_details": i, "disparity_details": check_match}


                # ++++++++ SHOULD NO MACTH EXISTS +++++++++++++++++
                # if check_match["detail"]["result"] == True:
                #     break

    return all_image_details



async def add_label_image(request, file_image, username, db):

    get_user_id = db.query(models.Users).filter(models.Users.username == username)

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
    get_url= await s3Bucket.s3_upload_label(file_image, bucket_folder_path)

    label_images = models.ImageLabels(label=request.label.lower(), user_id=get_user_id.first().id)
    db.add(label_images)
    db.commit()
    db.refresh(label_images)

    images = models.Images(
        label= request.label.lower(), ingredient= request.ingredient.lower(), image_path= get_url,
        image_label_id= label_images.id
    )

    db.add(images)
    db.commit()
    db.refresh(images)




async def update_label_image(request, file_image, username, db):

    get_user_id = db.query(models.Users).filter(models.Users.username == username)

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
    get_url= await s3Bucket.s3_upload_label(file_image, bucket_folder_path)

    images = models.Images(
        label= request.label.lower(), ingredient= request.ingredient.lower(), image_path= get_url,
        image_label_id= request.label_id
    )

    db.add(images)
    db.commit()
    db.refresh(images)



async def replace_label_image(request, file_image, username, db):
    get_user_id = db.query(models.Users).filter(models.Users.username == username)

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

    images = db.query(models.Images).filter(models.Images.id == request.id)

    bucket_folder_path = f'users/{get_user_id.first().id}/label_images'
    await s3Bucket.s3_upload_replacement_label(file_image, images.first().image_path, bucket_folder_path)

    update_image= {'ingredient': request.ingredient}
    images.update(update_image)
    db.commit()

