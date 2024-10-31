from fastapi import FastAPI
from router.SportEventRouter import sport_router

app = FastAPI()
app.include_router(sport_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
