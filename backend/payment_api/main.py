from fastapi import FastAPI,Depends,Request,HTTPException,Header,status
from pydantic import BaseModel
from dotenv import load_dotenv
import sys 
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from jose import JWTError,jwt
import time
import hmac
import hashlib
from backend.payment_api.auth import create_refresh_token,create_access_token 
from backend.database.jwt_db.jwt_core import safe_first_refresh_token,get_user_refresh_token,update_refresh_token



pay_app = FastAPI()




