from fastapi import Depends, FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import JWTError
import jwt
from  pydantic import BaseModel
from services.calculate_area import area_rectangle
from services.weather_service import get_weather
from services.currency_convertor import currency_convertor
from services.isPlalindrome import isPlaindrome
from services.wikipedia_summary import fetch_Summary
from fastapi import status , HTTPException
from auth.auth_service import UserRouter
# from auth.api_service import apiServiceRouter # update it later if needed
from auth.utils import get_current_user
from slowapi import Limiter ,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from slowapi.middleware import SlowAPIMiddleware 




def get_user_or_ip_identifier(request: Request) -> str:
    # Check if we attached a user to the request state during authentication
    if hasattr(request.state, "user_name"):
        return f"user:{request.state.user_id}"
    return get_remote_address(request) # Fallback for public routes

# limiter = Limiter(key_func=get_remote_address)
# limiter = Limiter(key_func=get_user_or_ip_identifier)
limiter = Limiter(key_func=lambda request: request.client.host)
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

@app.middleware("http")
async def extract_user_for_rate_limiter(request: Request, call_next):
    # 1. Look for the Bearer Token in the headers
    auth_header = request.headers.get("Authorization")
    SECRET_KEY = "lets_learn"
    ALGORITHM ="HS256"
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            # 2. Decode the token to see who this is
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            
            if username:
                # 3. 🟢 CREATE IT HERE! This sets it for THIS specific incoming service request!
                request.state.user_id = username
                
        except JWTError:
            pass # Let the route handle throwing unauthorized errors if needed
            
    response = await call_next(request)
    return response



template = Jinja2Templates(directory="templates")

# logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),       
        logging.FileHandler("local_api.log") 
    ]
)


logger = logging.getLogger("APIForge")

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
@limiter.limit("3/minute")
def area(request:Request,data:Area,current_user:str = Depends(get_current_user)):
    try:
        value = area_rectangle(length=data.length,width=data.width)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="Enter value greater than 0"
        )
    logger.info(f"User '{current_user.user_name}' requested area calculation.")
    return value 


@app.post("/weather")
@limiter.limit("3/minute")
def weather(request:Request,data:Weather,current_user:str = Depends(get_current_user)):
    try:
         value = get_weather(city=data.city)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "city not found"
        )
    logger.info(f"User '{current_user.user_name}' requested weather service.")
    return value


@app.post("/currency_convertor")
@limiter.limit("3/minute")
def convertor(request:Request,data:Currency,current_user:str = Depends(get_current_user)):
    try :
        value = currency_convertor(value=data.value,currency=data.currency)
    except ValueError as e:
        print(e) # debug💀💀💀💀
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" currency not found")
    logger.info(f"User '{current_user.user_name}' requested currency convertor service")
    return value


@app.post("/isPalindrome")
@limiter.limit("3/minute")
def palindrome(request:Request,data:Palindrome,current_user:str = Depends(get_current_user)):

    try:
        value = isPlaindrome(word=data.string)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Empty input")
    logger.info(f"User '{current_user.user_name}' requested palindrome service")
    return value


@app.post("/wikipedia")
@limiter.limit("3/minute")
def wikipedia(request:Request,data:Wikipedia,current_user:str = Depends(get_current_user)):
    try:
        value = fetch_Summary(topic=data.topic)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    logger.info(f"User '{current_user.user_name}' requested wikipedia service")
    return value


