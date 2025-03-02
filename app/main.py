from fastapi import FastAPI
from .database import Base, engine 
from app.api.v1.main_router import router 

app = FastAPI(swagger_ui_parameters={"theme": "dark"})

Base.metadata.create_all(bind = engine)

app.include_router(router)