from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Basic FastAPI Endpoints",
    version="1.0.0"
)

class Student(BaseModel):
    id: int
    name: str
    course: str
    age: int

students_db = [
    Student(id=1, name="Gaurav Sharma", course="Data Science", age=20),
    Student(id=2, name="Sarthak Patel", course="Data Science", age=21)
]

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Basics API!"}

@app.get("/students")
async def get_all_students():
    return {"status": "success", "total": len(students_db), "students": students_db}

@app.post("/students", status_code=201)
async def create_student(student: Student):
    students_db.append(student)
    return {
        "message": "Student created successfully",
        "student": student
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
