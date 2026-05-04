from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import UserCreate, UserLogin, UserResponse
router = APIRouter()

@router.post("/register")
async def register(user_data: UserCreate):
    db = get_db()#mongo db use this that was i implement it here. and it was getting the data from database.py file
    existing_user = await db["users"].find_one(#check if email already exist or not 
        {"email": user_data.email}
    )
    if existing_user:#if email exist then it will raise the error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already exists"
        )
    hashed = hash_password(user_data.password)

    new_user = {#create new user and insert into database
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed,
        "phone":user_data.phone,
        "age": user_data.age,
        "gender": user_data.gender,
        "is_active": True,
        "created_at":datetime.now(timezone.utc)

    }

    result = await db["users"].insert_one(new_user)#after creating new user it will generate the token for that user and return the response

    token = create_access_token({#create token for new user
        "user_id": str(result.inserted_id),
        "email":user_data.email
    })

    return {#return the response after registration
        "message":"registration sussefull",
        "token": token,
        "user":{
            "id":str(result.inserted_id),
            "name":user_data.name,
            "email": user_data.email
        }
    }

@router.post("/login")#login user and generate token for that user and return the response
async def login(user_data: UserLogin):
    db = get_db()

    user = await db["users"].find_one(#check if email exist or not
        {"email":user_data.email}
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,#if email not exist then it will raise the error
            detail="Invalid email or password"

        )
    is_valid = verify_password(user_data.password,user["password"])#check if password is correct or not
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token = create_access_token({
        "user_id":str(user["_id"]),
        "email": user["email"]
    })
    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }

@router.get("/me")#this is the endpoint for getting the current user details and it will be implemented in future
async def get_me():
    return {"message": "coming soon"}
