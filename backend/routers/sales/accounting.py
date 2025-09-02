from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db


router= APIRouter(prefix="/sales/accounting",tags=["Accounting"])