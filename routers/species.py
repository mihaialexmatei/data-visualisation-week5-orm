from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models.species import Species, SpeciesCreate
from repositories.species import SpeciesRepository

router = APIRouter(prefix="/species", tags=["Species"])

def get_repo(session: Annotated[Session, Depends(get_session)]) -> SpeciesRepository:
    return SpeciesRepository(session)

@router.get("/", response_model=List[Species])
async def get_species(repo: Annotated[SpeciesRepository, Depends(get_repo)]):
    """Get all species."""
    return repo.get_all()

@router.post("/", response_model=Species, status_code=201)
async def add_species(payload: SpeciesCreate, repo: Annotated[SpeciesRepository, Depends(get_repo)]):
    """Add a new species."""
    return repo.insert(payload)