from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/certifications", tags=["certifications"])

@router.get("/", response_model=List[schemas.CertificationSchema])
def get_certifications(db: Session = Depends(get_db)):
    return db.query(models.Certification).all()

@router.post("/", response_model=schemas.CertificationSchema, status_code=status.HTTP_201_CREATED)
def create_certification(cert: schemas.CertificationCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_cert = models.Certification(**cert.dict())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

@router.put("/{cert_id}", response_model=schemas.CertificationSchema)
def update_certification(cert_id: int, cert: schemas.CertificationCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_cert = db.query(models.Certification).filter(models.Certification.id == cert_id).first()
    if not db_cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    
    for key, value in cert.dict().items():
        setattr(db_cert, key, value)
    
    db.commit()
    db.refresh(db_cert)
    return db_cert

@router.delete("/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(cert_id: int, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_cert = db.query(models.Certification).filter(models.Certification.id == cert_id).first()
    if not db_cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    
    db.delete(db_cert)
    db.commit()
    return None
