from fastapi import FastAPI
from .userRegi import renew, regi

app = FastAPI()

# renew.pyのrouterを登録
app.include_router(renew.router)

#regi.pyのrouterを登録
app.include_router(regi.router)