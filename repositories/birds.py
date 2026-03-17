from fastapi import HTTPException
from sqlmodel import Session, select
from models.birds import Bird, BirdCreate
from models.species import Species

class BirdRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Bird)).all()

    def insert(self, payload: BirdCreate):
        # Check if species exists
        species = self.session.get(Species, payload.species_id)
        if not species:
            raise HTTPException(status_code=404, detail="Species not found")

        item = Bird.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item