from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/contact", tags=["contact"])

@router.post("/", response_model=schemas.ContactMessageSchema, status_code=status.HTTP_201_CREATED)
def send_message(message: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    db_message = models.ContactMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/", response_model=List[schemas.ContactMessageSchema])
def get_messages(current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    return db.query(models.ContactMessage).all()

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: int, 
    current_admin: models.Admin = Depends(auth.get_current_admin), 
    db: Session = Depends(get_db)
):
    db_message = db.query(models.ContactMessage).filter(models.ContactMessage.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(db_message)
    db.commit()
    return None
