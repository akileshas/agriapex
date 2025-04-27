from fastapi import FastAPI
from routes import data

app = FastAPI()

# all sub-routes
app.include_router(data.routes, prefix="/data")

@app.get("/")
def testing():
    res = {
        "msg": "Testing the handshake !"
    }

    return res
