from fastapi import Depends, FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from  pydantic import BaseModel
from services.calculate_area import area_rectangle
from services.weather_service import get_weather
from services.currency_convertor import currency_convertor
from services.isPlalindrome import isPlaindrome
from services.wikipedia_summary import fetch_Summary
from fastapi import status , HTTPException
from auth.auth_service import UserRouter
from auth.api_service import apiServiceRouter
from jose import JWTError, jwt
from auth.utils import get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


template = Jinja2Templates(directory="templates")

# auth router
app.include_router(router=UserRouter)
# app.include_router(router=apiServiceRouter)  # update later if needed

class Area(BaseModel):
    length :float
    width : float

class Weather(BaseModel):
    city :str

class Currency(BaseModel):
    currency:str
    value:float

class Palindrome(BaseModel):
    string:str

class Wikipedia(BaseModel):
    topic:str

@app.get("/")
def home(request:Request):
    return template.TemplateResponse(
        request=request,
        name = 'index.html'
    )




@app.post("/calculate_area")
def area(data:Area,current_user:str = Depends(get_current_user)):
    try:
        value = area_rectangle(length=data.length,width=data.width)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="Enter value greater than 0"
        )
    return value


@app.post("/weather")
def weather(data:Weather,current_user:str = Depends(get_current_user)):
    try:
         value = get_weather(city=data.city)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "city not found"
        )
    return value


@app.post("/currency_convertor")
def convertor(data:Currency,current_user:str = Depends(get_current_user)):
    try :
        value = currency_convertor(value=data.value,currency=data.currency)
    except ValueError as e:
        print(e) # debug💀💀💀💀
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" currency not found")

    return value


@app.post("/isPalindrome")
def palindrome(data:Palindrome,current_user:str = Depends(get_current_user)):

    try:
        value = isPlaindrome(word=data.string)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Empty input")
    return value


@app.post("/wikipedia")
def wikipedia(data:Wikipedia,current_user:str = Depends(get_current_user)):
    try:
        value = fetch_Summary(topic=data.topic)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return value


