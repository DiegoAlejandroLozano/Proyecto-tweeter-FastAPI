#Python nativo
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

#models
class UserBase(BaseModel):
    user_id:UUID = Field(...)
    email:EmailStr = Field(...)

class UserLogin(UserBase):
    password:str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):    
    
    first_name:str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name:str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date:Optional[date] = Field(default=None)

class Tweet(BaseModel):
    tweet_id:UUID = Field(...)
    content:str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    create_at:datetime = Field(default=datetime.now())
    update_at:Optional[datetime] = Field(default=None)
    by:User = Field(...)

#Path operations

@app.get(path="/")
def home():
    return {
        "twitter API":"Working!"
    }

##users

@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["User"]
)
def signup():
    pass

@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_CREATED,
    summary="Login a User",
    tags=["User"]
)
def login():
    pass

@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_CREATED,
    summary="Show all users",
    tags=["User"]
)
def show_all_users():
    pass

@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_CREATED,
    summary="Show a User",
    tags=["User"]
)
def show_a_user():
    pass

@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_CREATED,
    summary="Delete a User",
    tags=["User"]
)
def delete_a_user():
    pass

@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_CREATED,
    summary="Update a User",
    tags=["User"]
)
def update_a_user():
    pass

##Tweets


