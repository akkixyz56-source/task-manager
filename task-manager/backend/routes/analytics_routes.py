from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from auth import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tasks")
def get_task_analytics(db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):

    # Total tasks (only user's projects)
    total_tasks = db.query(models.Task).join(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).count()

    completed = db.query(models.Task).join(models.Project).filter(
        models.Project.owner_id == current_user.id,
        models.Task.status == "Completed"
    ).count()

    pending = db.query(models.Task).join(models.Project).filter(
        models.Project.owner_id == current_user.id,
        models.Task.status == "Pending"
    ).count()

    in_progress = db.query(models.Task).join(models.Project).filter(
        models.Project.owner_id == current_user.id,
        models.Task.status == "In Progress"
    ).count()

    # Tasks per project
    tasks_per_project = db.query(
       models.Project.project_name,
       func.count(models.Task.id)
    ).join(models.Task).filter(
       models.Project.owner_id == current_user.id
    ).group_by(models.Project.project_name).all()

    tasks_per_project_data = [
    {"project_name": name, "task_count": count}
    for name, count in tasks_per_project
    ]

    return {
    "total_tasks": total_tasks,
    "completed": completed,
    "pending": pending,
    "in_progress": in_progress,
    "tasks_per_project": tasks_per_project_data
    }