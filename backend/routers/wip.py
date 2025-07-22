# backend/routers/wip.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.wip import WIPCreate, WIPUpdate, WIPOut
from backend.dependencies import get_db
from backend.crud import wip as wip_crud  #  import CRUD functions

router = APIRouter(prefix="/wip", tags=["wip"])


@router.post("/", response_model=WIPOut)
def start_wip(wip: WIPCreate, db: Session = Depends(get_db)):
    return wip_crud.create_wip(db, wip)


@router.put("/{wip_id}", response_model=WIPOut)
def update_wip(wip_id: int, update: WIPUpdate, db: Session = Depends(get_db)):
    return wip_crud.update_wip(db, wip_id, update)
