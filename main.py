from fastapi import FastAPI
app = FastAPI()

#decorator:to define the path and method
@app.get("/welcome") # اي حد يفتح الرابط ده هيشوف الرسالة دي
def welcome():
    return{
        "message" : "hello World!"
    }