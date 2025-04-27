from fastapi import FastAPI
from routes import data

app = FastAPI()

# all sub-routes
app.include_router(data.router, prefix="/data")

@app.get("/")
def testing():
    res = {
        "msg": "Testing the handshake !"
    }

    return res
