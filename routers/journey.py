from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/journey", tags=["journey"])

@router.get("/", response_model=List[schemas.JourneySchema])
def get_journeys(db: Session = Depends(get_db)):
    return db.query(models.Journey).all()

@router.post("/", response_model=schemas.JourneySchema, status_code=status.HTTP_201_CREATED)
def create_journey(journey: schemas.JourneyCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_journey = models.Journey(**journey.dict())
    db.add(db_journey)
    db.commit()
    db.refresh(db_journey)
    return db_journey

@router.put("/{journey_id}", response_model=schemas.JourneySchema)
def update_journey(journey_id: int, journey: schemas.JourneyCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_journey = db.query(models.Journey).filter(models.Journey.id == journey_id).first()
    if not db_journey:
        raise HTTPException(status_code=404, detail="Journey not found")
    
    for key, value in journey.dict().items():
        setattr(db_journey, key, value)
    
    db.commit()
    db.refresh(db_journey)
    return db_journey

@router.delete("/{journey_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journey(journey_id: int, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_journey = db.query(models.Journey).filter(models.Journey.id == journey_id).first()
    if not db_journey:
        raise HTTPException(status_code=404, detail="Journey not found")
    
    db.delete(db_journey)
    db.commit()
    return None
