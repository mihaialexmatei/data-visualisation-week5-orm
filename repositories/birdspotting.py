from fastapi import HTTPException
from sqlmodel import Session, select
from models.birdspotting import Birdspotting, BirdspottingCreate
from models.birds import Bird

class BirdspottingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Birdspotting)).all()

    def get_one(self, id: int):
        item = self.session.get(Birdspotting, id)
        if not item:
            raise HTTPException(status_code=404, detail="Birdspotting record not found")
        return item

    def insert(self, payload: BirdspottingCreate):
        # Check if bird exists
        bird = self.session.get(Bird, payload.bird_id)
        if not bird:
            raise HTTPException(status_code=404, detail="Bird not found")

        item = Birdspotting.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item