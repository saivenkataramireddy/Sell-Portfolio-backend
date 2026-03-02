from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("/", response_model=List[schemas.SkillSchema])
def get_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()

@router.post("/", response_model=schemas.SkillSchema, status_code=status.HTTP_201_CREATED)
def create_skill(skill: schemas.SkillCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_skill = models.Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.put("/{skill_id}", response_model=schemas.SkillSchema)
def update_skill(skill_id: int, skill: schemas.SkillCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill.dict().items():
        setattr(db_skill, key, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: int, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(db_skill)
    db.commit()
    return None
