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

# app = FastAPI()

# cred = credentials.Certificate("animengine-9ccdf-firebase-adminsdk-pajcy-1c1e1bdc8d.json")
# firebase_admin.initialize_app(cred)


# @app.post("/sign-in")
# def sign_in(email: str, password: str):
#     try:
#         user = auth.sign_in_with_email_and_password(email, password)
#         return {"message": "Sign-in successful", "user": user}
#     except auth.AuthError:
#         return {"message": "Invalid email or password"}


app = FastAPI()
cred = credentials.Certificate('animengine-9ccdf-firebase-adminsdk-pajcy-1c1e1bdc8d.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase-config.json')))
allow_all = ['*']
app = FastAPI()
allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)


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
    print("OK>")
    req = await request.json()
    print("OK>2")
    email = req['email']
    password = req['password']
    if email is None or password is None:
        return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
    try:
        user = auth.create_user(
            email="dummy@gmail.com",
            password="12345678"
        )
        return JSONResponse(content={'message': f'Successfully created user {user.uid}'}, status_code=200)
    except:
        return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)


@app.post("/login", include_in_schema=False)
async def login(request: Request):
    req_json = await request.json()
    # request_body = request.body().
    # print(request.json())
    # req_json = json.loads(request_body)


    email = req_json['email']
    password = req_json['password']
    try:
        print("OK>2")
        user = pb.auth().sign_in_with_email_and_password("bentest@gmail.com", "bentest@gmail.com")
        jwt = user['idToken']
        return JSONResponse(content={'token': jwt}, status_code=200)
    except:
        print("OK>3")
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)


# ping endpoint
@app.get("/ping", include_in_schema=False)
async def validate(request: Request):
    headers = request.headers
    jwt = headers.get('authorization')
    print(f"jwt:{jwt}")
    user = auth.verify_id_token(jwt)
    return user["uid"]


if __name__ == "__main__":
    #uvicorn.run("main:app")
    uvicorn.run(app=app,host="192.168.56.1", port=8080)
