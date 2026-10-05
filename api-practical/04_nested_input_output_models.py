from typing import List, Optional
from datetime import date
from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(
    title="Nested Pydantic Models",
    version="1.0.0"
)

class Address(BaseModel):
    street: str = Field(..., example="123 Science Park Road")
    city: str = Field(..., example="Mumbai")
    state: str = Field(..., example="Maharashtra")
    pincode: int = Field(..., example=400001)

class TaskItem(BaseModel):
    item_id: int
    title: str
    is_completed: bool = False

class UserProfile(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    address: Address
    pending_tasks: List[TaskItem] = []

class UserProfileResponse(BaseModel):
    status: str
    user: UserProfile
    task_count: int

users_db: List[UserProfile] = []

@app.get("/")
def home():
    return {"message": "Nested Models API Service"}

@app.post("/users", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(user: UserProfile):
    users_db.append(user)
    return UserProfileResponse(
        status="User profile created successfully",
        user=user,
        task_count=len(user.pending_tasks)
    )

@app.get("/users", response_model=List[UserProfile])
def list_users():
    return users_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
