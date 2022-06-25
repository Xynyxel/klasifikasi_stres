from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def read_test():
    return {"Hello": "test"}

@app.get("/lagi")
def read_test():
    return {"Hello": "lagi"}

@app.get("/satu_lagi")
def read_test():
    return {"Hello": "satu_lagi"}

@app.get("/lah")
def read_test():
    return {"Hello": "lah"}