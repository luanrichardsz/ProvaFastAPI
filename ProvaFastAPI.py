from fastapi import FastAPI
from crud import router
from database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router)