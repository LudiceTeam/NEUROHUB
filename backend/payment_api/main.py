from fastapi import FastAPI,Depends,Request,HTTPException,Header,status
from fastapi.security import OAuth2
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from dotenv import load_dotenv
import sys 
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.util import get_remote_address
from jose import JWTError,jwt
import time
import hmac
import hashlib
from backend.payment_api.auth import create_refresh_token,create_access_token 
from backend.database.jwt_db.jwt_core import safe_first_refresh_token,get_user_refresh_token,update_refresh_token
from backend.database.payment_db.payment_core import create_payment 
import requests

pay_app = FastAPI()
limiter = Limiter(key_func=get_remote_address)



class CreatePayment(BaseModel):
    user_id:str
    tarif:str


load_dotenv()



CLOUDPAYMENTS_PUBLIC_ID = os.getenv("CLOUDPAYMENTS_PUBLIC_ID")
CLOUDPAYMENTS_API_SECRET = os.getenv("CLOUDPAYMENTS_API_SECRET")
api_token = os.getenv("API_TOKEN")



def generate_cloudpayments_link(
    payment_id: str,
    user_id: str,
    price: int,
    tariff: str,
) -> str:
    url = "https://api.cloudpayments.ru/orders/create"

    payload = {
        "Amount": price,
        "Currency": "RUB",
        "Description": f"Оплата тарифа {tariff}",
        "InvoiceId": payment_id,
        "AccountId": f"tg_{user_id}",
        "SuccessRedirectUrl": "https://your-site.com/payment/success",
        "FailRedirectUrl": "https://your-site.com/payment/fail",
        "JsonData": {
            "tg_user_id": user_id,
            "tariff": tariff
        }
    }

    resp = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(CLOUDPAYMENTS_PUBLIC_ID, CLOUDPAYMENTS_API_SECRET),
        timeout=15
    )

    data = resp.json()

    if not resp.ok or not data.get("Success"):
        raise HTTPException(status_code=500, detail="CloudPayments error")

    return data["Model"]["Url"]

def verify_token(recieved_token:str) -> bool:
    if api_token != recieved_token:
        return False
    return True

@limiter.limit("20/minute")
@pay_app.post("/create-payment")
async def create_payment_api(request:Request,req:CreatePayment,token:str = Header(...)):
    if not verify_token(token):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "FORBIDDEN")
    price = None
    if req.tarif == "basic":
        price = 400
    elif req.tarif == "premium":
        price = 1000
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Invalid json")
    

    payment_id:str = await create_payment(
        price = price,
        user_id = req.user_id
    )

    link = generate_cloudpayments_link(
        payment_id,
        req.user_id,
        price,
        req.tarif
    )
    return {
        "status":"ok",
        "link":link
    }
    




