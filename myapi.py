from fastapi import FastAPI
app=FastAPI()
students={
    1:{
        "name":"john",
        "age":17,
        "class":"year 12",
    }
}
@app.get("/")
def index():
    return{"Name":"First Data"}
@app.get("/get-student/{student_id}")
def get_student(student_id:int): 
    return students[student_id]

