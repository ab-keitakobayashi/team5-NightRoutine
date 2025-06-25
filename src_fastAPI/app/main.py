from fastapi import FastAPI
from userRegi import renew

app = FastAPI()

# renew.pyのrouterを登録
app.include_router(renew.router)