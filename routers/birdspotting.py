from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models.birdspotting import Birdspotting, BirdspottingCreate
from repositories.birdspotting import BirdspottingRepository

router = APIRouter(prefix="/birdspotting", tags=["Birdspotting"])

def get_repo(session: Annotated[Session, Depends(get_session)]) -> BirdspottingRepository:
    return BirdspottingRepository(session)

@router.get("/", response_model=List[Birdspotting])
async def get_all(repo: Annotated[BirdspottingRepository, Depends(get_repo)]):
    """Get all birdspotting observations."""
    return repo.get_all()

@router.get("/{id}", response_model=Birdspotting)
async def get_one(id: int, repo: Annotated[BirdspottingRepository, Depends(get_repo)]):
    """Get a single birdspotting observation by ID."""
    return repo.get_one(id)

@router.post("/", response_model=Birdspotting, status_code=201)
async def add_birdspotting(payload: BirdspottingCreate, repo: Annotated[BirdspottingRepository, Depends(get_repo)]):
    """Add a new birdspotting observation linked to an existing bird."""
    return repo.insert(payload)