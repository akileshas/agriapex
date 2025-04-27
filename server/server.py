from fastapi import FastAPI
from routes import (
    data,
    weather,
    model
)

app = FastAPI()

# all sub-routes
app.include_router(data.routes, prefix="/data")
app.include_router(weather.routes, prefix="/weather")
app.include_router(model.routes, prefix="/model")


@app.get("/")
def testing():
    res = {
        "msg": "Testing the handshake !"
    }

    return res
