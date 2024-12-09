from fastapi import FastAPI
from routes import teacher, student

app = FastAPI()

app.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
app.include_router(student.router, prefix="/student", tags=["Student"])