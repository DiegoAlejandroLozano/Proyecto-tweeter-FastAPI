#Python nativo
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import Path
from fastapi import HTTPException

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

class UserRegister(User):
    password:str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id:UUID = Field(...)
    content:str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    create_at:datetime = Field(default=datetime.now())
    updated_at:Optional[datetime] = Field(default=None)
    by:User = Field(...)

class LoginUser(BaseModel):
    email:EmailStr = Field(...)
    password:str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class UpdateUser(BaseModel):
    email:EmailStr=Field(...)
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


#Path operations

##users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["User"]
)
def signup(user:UserRegister=Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters:
        -Request body parameter
            -user:UserRegister

    Returns a json with the basic user information:
        -user_id:UUID
        -email:EmailStr
        -first_name:str
        -last_name:str
        -birth_date:datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results =json.loads(f.read())
        tweet_dict = user.dict()
        tweet_dict["user_id"] = str(tweet_dict["user_id"])
        tweet_dict["birth_date"] = str(tweet_dict["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results, indent=2))
        return user


### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["User"]
)
def login(login:LoginUser=Body(...)):
    """
    login

    This function is in charge of verifying if a user is registered. To carry out the verification, the 
    email and password are compared with the email and password of the users who have already been registered.

    Parameters:
        -Request body parameter
            -login:LoginUser

    Returns a json with the basic user information:
        -user_id:UUID
        -email:EmailStr
        -first_name:str
        -last_name:str
        -birth_date:datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        for result in results:
            if login.email == result["email"]:
                if login.password == result["password"]:
                    del result['password']
                    return result
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="The password does not match"
                    )                 
        #If the email does not match any user, an exception is raised
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The email is not registered"
        )   

### Show all the users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["User"]
)
def show_all_users():
    """
    This path operation shows all users in the app

    Parameters:
        -

    Return a json list with all users in the app, with the following keys
        -user_id:UUID
        -email:EmailStr
        -first_name:str
        -last_name:str
        -birth_date:datetime
    """
    with open('users.json', "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["User"]
)
def show_a_user(
    user_id:str=Path(
        ...,
        title="Id user"
    )
):
    """
    show_a_user

    This function is responsible for finding a user in the .json file through its ID, which is passed as a path parameter

    Parameters:
        -Request path parameter
            -user_id:str

    Returns a json with the basic user information:
        -user_id:UUID
        -email:EmailStr
        -first_name:str
        -last_name:str
        -birth_date:datetime
    """

    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        for result in results:
            if result["user_id"] == user_id:
                del result["password"]
                return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found"
        )   

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    #response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["User"]
)
def delete_a_user(
    user_id:str=Path(
        ...,
        title="ID user"
    )
):
    """
    delete_a_user

    This function is responsible for removing a user from the .json file, starting from the ID specified in the URL

    Parameters:
        -Request path parameter
            -user_id:str

    Returns a json with the basic information of the deleted user:
        -user_id:UUID
        -email:EmailStr
        -first_name:str
        -last_name:str
        -birth_date:datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())        
        for i in range(len(results)):
            if results[i]["user_id"] == user_id:
                deleted_user = results.pop(i)
                f.truncate(0)
                f.seek(0)
                f.write(json.dumps(results, indent=2))
                del deleted_user["password"]
                return deleted_user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found"
        )
        

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=UpdateUser,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["User"]
)
def update_a_user(
    user_id:str = Path(...),
    user_updated:UpdateUser = Body(...)
):
    """
    update_a_user

    This function is used to update user fields. To choose which user the data will be updated to, the ID passed in the path is used.

    Parameters:
        -Request path parameter
            -user_id:str
        -Request body parameter
            -user_updated:UpdateUser

    Returns a json with the updated information:
        -email:EmailStr
        -first_name:str
        -last_name:str
        -birth_date:datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dic = user_updated.dict()
        for i in range(len(results)):
            if results[i]["user_id"] == user_id:
                results[i] = {
                    "user_id":results[i]["user_id"],
                    "email": user_dic["email"],
                    "first_name": user_dic["first_name"],
                    "last_name": user_dic["last_name"],
                    "birth_date": str(user_dic["birth_date"]),
                    "password": results[i]["password"]
                }                 
                f.truncate(0)
                f.seek(0)
                f.write(json.dumps(results, indent=2))
                return user_updated
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found"
        )

##Tweets

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=['Tweets']

)
def home():
    """
    This path operation shows all tweets in the app

    Parameters:
        -

    Return a json list with all tweets in the app, with the following keys
        -tweet_id:UUID
        -content:str
        -create_at:datetime
        -updated_at:Optional[datetime]
        -by: User
    """
    with open('tweets.json', "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a Tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet:Tweet=Body(...)):
    """
    Post a tweet

    This path operation post a tweet in the app

    Parameters:
        -Request body parameter
            -tweet: Tweet

    Returns a json with the basic tweet information:
        -tweet_id:UUID
        -content:str
        -create_at:datetime
        -updated_at:Optional[datetime]
        -by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results =json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["create_at"] = str(tweet_dict["create_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results, indent=2))
        return tweet

### Show a Tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(
    tweet_id:str=Path(
        ...,
        title="Tweet ID"
    )
):
    """
    show_a_tweet

    This function is responsible for displaying a specific Tweet, depending on the ID passed in the URL

    Parameters:
        -Request PATH parameter
            -tweet_id:str

    Returns a json with the basic tweet information:
        -tweet_id:UUID
        -content:str
        -create_at:datetime
        -updated_at:Optional[datetime]
        -by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        for result in results:
            if result["tweet_id"] == tweet_id:
                return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The tweet was not found"
        )

### Delete a Tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(
    tweet_id:str = Path(
        ...,
        title="Tweet ID"
    )
):
    """
    show_a_tweet

    This function is responsible for deleting the Tweet indicated by the ID, which is passed through the URL

    Parameters:
        -Request PATH parameter
            -tweet_id:str

    Returns a json with the basic information of the tweet that was deleted:
        -tweet_id:UUID
        -content:str
        -create_at:datetime
        -updated_at:Optional[datetime]
        -by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        content = json.loads(f.read())
        for i in range(len(content)):
            if content[i]["tweet_id"] == tweet_id:
                deleted_tweet = content.pop(i)
                f.truncate(0)
                f.seek(0)
                f.write(json.dumps(content, indent=2))
                return deleted_tweet
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The tweet was not found"
        )

### Update a Tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass
