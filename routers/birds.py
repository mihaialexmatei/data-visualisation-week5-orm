from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models.birds import Bird, BirdCreate
from repositories.birds import BirdRepository

router = APIRouter(prefix="/birds", tags=["Birds"])

def get_repo(session: Annotated[Session, Depends(get_session)]) -> BirdRepository:
    return BirdRepository(session)

@router.get("/", response_model=List[Bird])
async def get_birds(repo: Annotated[BirdRepository, Depends(get_repo)]):
    """Get all birds."""
    return repo.get_all()

@router.post("/", response_model=Bird, status_code=201)
async def add_bird(payload: BirdCreate, repo: Annotated[BirdRepository, Depends(get_repo)]):
    """Add a new bird linked to an existing species."""
    return repo.insert(payload)