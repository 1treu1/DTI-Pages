#Python
from email.policy import default
from turtle import title
from typing import Optional
import pandas as pd
from enum import Enum
#Pydantic
from pydantic import BaseModel, Field
#FastAPI
from fastapi import FastAPI, Body, File, Query, UploadFile,Form, Path
app = FastAPI()

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
#Models
class Location(BaseModel):
    city: str
    state: str
    country: str
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miuel"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=2
    )
    hair_color: Optional[HairColor] = Field(default=None,example="black")
    is_married: Optional[bool] = Field(default=None,example=False)
    # class Config :
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "García Martoni",
    #             "age": 21,
    #             "hair_color"
    #             "blonde"
    #             "is_married " : False
    #         }
    #     }

@app.get("/") #Path decoration decorator
def home(): #"Path Operation Funtion"
    return {"Hello": "World"}

#request and Response body

@app.post("/person/new") #crea personas nuevas
def create_person(person: Person = Body(...)): #Body(...) Parametro obligatorio
    return person

#Validacione: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title = "Person Name",
        description= "This is the person name. It's between 1 an 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )
):
    return {name:age}
#Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        description="This is the person id. It's required"
        )
):
    return{person_id: "It exists!"}

# Validation: Body Parameters or request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt = 0
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    # return results
    return person

# @app.post('/uploadfile/')
# async def create_data_file(
#         experiment: str = Form(...),
#         file_type: str = Form(...),
#         file_id: str = Form(...),
#         data_file: UploadFile = File(...),
#         ):
    
#     #decoded = base64.b64decode(data_file.file)
#     #decoded = io.StringIO(decoded.decode('utf-8'))
    
#     print(pd.read_csv(data_file.file, sep='\t'))

#     return {'filename': data_file.filename, 
#             'experiment':experiment, 
#             'file_type': file_type, 
#             'file_id': file_id}
