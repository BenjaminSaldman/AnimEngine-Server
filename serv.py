from http.client import HTTPException

import pyrebase
from fastapi import FastAPI
import uvicorn
import firebase_admin
import json

from firebase_admin import credentials, auth
from fastapi import FastAPI, Request
# from pyrebase import pyrebase
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# cred = credentials.Certificate('animengine-9ccdf-firebase-adminsdk-pajcy-1c1e1bdc8d.json')
# firebase = firebase_admin.initialize_app(cred)
cred = credentials.Certificate('animengine-9ccdf-firebase-adminsdk-pajcy-1c1e1bdc8d.json')
# firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase-config.json')))
app = FastAPI()
allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)
pb = pyrebase.initialize_app(json.load(open('firebase-config.json')))
allow_all = ['*']
app = FastAPI()


@app.get('/')
def hello_world():
    return {'hello': 'world'}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# signup endpoint

# login endpoint

# ping endpoint
@app.post("/signup", include_in_schema=False)
async def signup(request: Request):
    req = await request.json()
    email = req['email']
    password = req['password']
    if email is None or password is None:
        return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return JSONResponse(content={'message': f'Successfully created user {user.uid}'}, status_code=200)
    except:
        return HTTPException()


@app.post("/login", include_in_schema=False)
async def login(request: Request):
    req_json = await request.json()
    email = req_json['email']
    password = req_json['password']
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['localId']
        return JSONResponse(content={'token': jwt}, status_code=200)
    except:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)


# ping endpoint


@app.post("/ping", include_in_schema=False)
async def validate(request: Request):
    headers = request.headers
    jwt = headers.get('authorization')
    print(f"jwt:{jwt}")
    user = auth.verify_id_token(jwt)
    return user["uid"]

# Most of the code was taken from here: https://pythonalgos.com/python-firebase-authentication-integration-with-fastapi/

if __name__ == "__main__":
    # host should be your ipv4 address
    uvicorn.run("main:app", host="10.12.12.199")
# uvicorn.run(app=app, host="172.20.10.2", port=8080)
# uvicorn.run(app,host="172.20.10.2", port=53078)
