from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE PROJECT
@router.post("/")
def create_project(project: schemas.ProjectCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):

    new_project = models.Project(
        project_name=project.project_name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# GET ALL PROJECTS (ONLY USER'S)
@router.get("/")
def get_projects(db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):

    return db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).all()


# UPDATE PROJECT
@router.put("/{project_id}")
def update_project(project_id: int,
                   project: schemas.ProjectCreate,
                   db: Session = Depends(get_db),
                   user_email: str = Depends(get_current_user)):

    user = db.query(models.User).filter(models.User.email == user_email).first()

    db_project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == user.id
    ).first()

    if not db_project:
        return {"error": "Project not found"}

    db_project.project_name = project.project_name
    db_project.description = project.description

    db.commit()
    db.refresh(db_project)

    return {
        "id": db_project.id,
        "project_name": db_project.project_name,
        "description": db_project.description
    }


# DELETE PROJECT
@router.delete("/{project_id}")
def delete_project(project_id: int,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):

    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}