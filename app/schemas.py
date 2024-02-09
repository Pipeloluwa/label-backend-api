from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic.types import constr



#The reason why some base model relationship key variables of a class require to be wrapped in a List form to prevent validation error is because the foreign unique key for linking to
# two relationships of classes together is not residing in that class, hence, one has to put it inside a List

class SignUp(BaseModel):
    username: str
    email: str
    password: str

    class Config():
        from_attributes= True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config():
        from_attributes= True

class Info(BaseModel):
    username: constr(to_lower= True)
    email: str

    class Config():
        from_attributes= True

class Base(Info):
    password: str
    class Config():
        from_attributes= True


class PhoneNo(BaseModel):
    phone_no: str

class Otp(BaseModel):
    phone_or_email: str
    otp_token: str

class SendMailOnly(BaseModel):
    Subject: str
    Body: str
    To: str
    Cc: Optional[str]= None
    Bcc: Optional[str]= None

class SendMail(BaseModel):
    Subject: str
    To: str
    Cc: Optional[str]= None
    Bcc: Optional[str]= None
    Filename: Optional[str]= None
    class Config():
        from_attributes= True


class UsersBase(BaseModel):
    id: int
    activated: str
    username: str
    firstname: str
    lastname: str
    email: str
    phone_no: str
    # password: str
    registration_date: str

    class Config():
        from_attributes= True

class ImagesBase(BaseModel):
    id: int
    label: str
    ingredient: str
    image_path: str

    image_label_id: int
    class Config():
        from_attributes= True

class ImageLabels(BaseModel):
    id: int
    label: str

    user_id: int
    images: List[ImagesBase]
    users: UsersBase
    class Config():
        from_attributes= True

class Images(ImagesBase):
    image_label: ImageLabels
    class Config():
        from_attributes= True

class ImageLabelsBase(BaseModel):
    id: int
    label: str

    images: List[ImagesBase]
    class Config():
        from_attributes= True

class Users(UsersBase):
    image_label: List[ImageLabels]

    class Config():
        from_attributes = True



class ImageResultDetails(BaseModel):
    result: bool
    common: Optional[List]= None
    difference: Optional[List]= None
    match_score: float

class ImageResult(BaseModel):
    detail: List[ImageResultDetails]


class TokenDataUser(BaseModel):
    username: Optional[str]= None


# class UploadLabel(BaseModel):
#     label: str
#     # ingredient: str

class UpdateLabelImage(BaseModel):
    label_id: Optional[int]= None
    label: str
    ingredient: str

class ReplaceLabelImage(BaseModel):
    id: int
    ingredient: str
