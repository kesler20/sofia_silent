from fileinput import filename
from http.client import responses
from urllib import response
from boto3.dynamodb.conditions import Key
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import pandas as pd
from fastapi import Body, FastAPI, File, Body, UploadFile, Depends
import uuid
import json

try:
    from journal.cognito_auth.auth import get_current_user
    from journal.cognito_auth.auth import jwks
    from journal.cognito_auth.JWTBearer import JWTBearer
    from journal.config_file import *
    from journal.data_processing import calculate_SMA, calculate_trend_bounds, check_for_datetime, convert_tempfile_to_IO
    from journal.aws_CRUD import AWS_CRUD_API
except ModuleNotFoundError:
    from src.journal.cognito_auth.auth import get_current_user
    from src.journal.cognito_auth.auth import jwks
    from src.journal.cognito_auth.JWTBearer import JWTBearer
    from src.journal.config_file import *
    from src.journal.data_processing import calculate_SMA, calculate_trend_bounds, check_for_datetime, convert_tempfile_to_IO
    from src.journal.aws_CRUD import AWS_CRUD_API


####################################### INITIALISE APPLICATION AND CONFIGURE IT #######################################
app = FastAPI()
auth = JWTBearer(jwks)

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://0.0.0.0:3000",
    FRONT_END_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

api = AWS_CRUD_API(
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    DYNAMO_DB_NAME,
    S3_BUCKET_NAME
)

# Currently allowed file upload extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'xlsm', 'html'}


def allowed_file(filename: str):
    extension = filename.rsplit('.', 1)[1].lower()
    if extension in ALLOWED_EXTENSIONS:
        return extension
    else:
        return False

####################################### DEFINE CONTROLLER LOGIC AND ENDPOINTS #######################################


@app.get("/", tags=["root"])
async def read_root():
    response = RedirectResponse(url='/docs')
    return response


@app.post('/userFiles/CREATE', dependencies=[Depends(auth)])
async def handle_upload(user_files: UploadFile = File(...), user: str = Depends(get_current_user)):

    USER_DATA = pd.DataFrame()
    print(user_files.filename)

    ################## CONVERT USER FILES TO PANDAS DATA FRAME #################
    if(allowed_file(user_files.filename) == 'csv'):
        try:
            USER_DATA = pd.read_csv(user_files.file)
            USER_DATA = check_for_datetime(USER_DATA)
        except:
            return {"Error": "Is the file corrupted? Could not be decoded using UTF-8"}

        print(USER_DATA)
    elif (allowed_file(user_files.filename) in ['xlsx', 'xls', 'xlsm']):
        file_content = convert_tempfile_to_IO(user_files)
        USER_DATA = pd.read_excel(file_content)
        print(USER_DATA)
    else:
        print("\n\nWrongFileType ❌\n\n")
        return{"Error": "File type is not compatible"}

    ####################### Converts pandas dataframe to a json object for storage#####
    user_file_in_json = USER_DATA.to_json()
    fileID = str(user) + "/" + uuid.uuid4().hex

    api.create_user_file(user, fileID, user_files.filename, user_file_in_json)
    print('\n user file created successfully ✅\n')
    print(api.get_user_files(user)[-1])

    return {"filename": fileID}


@app.get('/userFiles/READ', dependencies=[Depends(auth)])
async def get_user_files(user: str = Depends(get_current_user)):
    user_files = api.get_user_files(user)
    print(user_files)

    return {'files found': user_files}


@app.post('/userFiles/UPDATE', dependencies=[Depends(auth)])
async def update_user_files(user_files: UploadFile = File(...), user: str = Depends(get_current_user)):

    USER_DATA = pd.DataFrame()
    print(user_files.filename)

    ################## CONVERT USER FILES TO PANDAS DATA FRAME #################
    if(allowed_file(user_files.filename) == 'csv'):
        try:
            USER_DATA = pd.read_csv(user_files.file)
            USER_DATA = check_for_datetime(USER_DATA)
        except:
            return {"Error": "Is the file corrupted? Could not be decoded using UTF-8"}

        print(USER_DATA)

    elif (allowed_file(user_files.filename) in ['xlsx', 'xls', 'xlsm']):

        file_content = convert_tempfile_to_IO(user_files)
        USER_DATA = pd.read_excel(file_content)
        print(USER_DATA)

    else:
        print("\n\nWrongFileType ❌\n\n")
        return{"Error": "File type is not compatible"}

    api.update_user_file(user, user_files.filename, USER_DATA.to_json())
    print('\n user file updated successfully ✅\n')
    print(list(filter(lambda file: file['filename'] ==
          user_files.filename, api.get_user_files(user))))

    return {'file updated': user_files.filename}


@app.delete('/userFiles/DELETE/', dependencies=[Depends(auth)])
async def delete_user_file(user: str = Depends(get_current_user), payload=Body(...)):

    ################### DELETE MATCHING FILES ########################
    api.delete_user_file(payload, user)
    deleted_files = list(
        filter(lambda file: file['filename'] == payload, api.get_user_files(user)))
    _ = print("\n no user files were found to delete ❌ \n") if deleted_files == [] else print(
        '\n user file deleted successfully ✅\n', deleted_files)


@app.post('/jobs/SMA', dependencies=[Depends(auth)])
async def calculate_simple_mooving_average(user: str = Depends(get_current_user), payload=Body(...)):
    ################# CALCULATE SMA FOR ALL THE CHANNELS SUBMITTED ##########

    sma = calculate_SMA(payload, 20, 30)
    print(sma)
    return {'job completed': [sma.to_json()]}


@app.post('/jobs/ANOVA', dependencies=[Depends(auth)])
async def calcualte_ANOVA(user: str = Depends(get_current_user)):
    pass
