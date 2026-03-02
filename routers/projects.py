from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[schemas.ProjectSchema])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@router.post("/", response_model=schemas.ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.put("/{project_id}", response_model=schemas.ProjectSchema)
def update_project(project_id: int, project: schemas.ProjectCreate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return None
