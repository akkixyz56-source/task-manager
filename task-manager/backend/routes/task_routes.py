from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE TASK
@router.post("/projects/{project_id}")
def create_task(project_id: int,
                task: schemas.TaskCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):

    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = models.Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        project_id=project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# GET TASKS OF A PROJECT
@router.get("/projects/{project_id}")
def get_tasks(project_id: int,
              db: Session = Depends(get_db),
              current_user: models.User = Depends(get_current_user)):

    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return db.query(models.Task).filter(
        models.Task.project_id == project_id
    ).all()


# UPDATE TASK
@router.put("/{task_id}")
def update_task(task_id: int,
                updated: schemas.TaskUpdate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):

    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated.title
    task.description = updated.description
    task.status = updated.status
    task.due_date = updated.due_date

    db.commit()
    return task


# DELETE TASK
@router.delete("/{task_id}")
def delete_task(task_id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):

    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}

@router.post("/{task_id}/assign")
def assign_task(task_id: int,
                body: schemas.AssignTask,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):

    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    user = db.query(models.User).filter(
        models.User.id == body.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task.assigned_user_id = body.user_id
    
    db.commit()
    db.refresh(task)

    return {"message": "Task assigned successfully"}

@router.get("/assigned/me")
def get_my_tasks(db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):

    tasks = db.query(models.Task).filter(
        models.Task.assigned_user_id == current_user.id
    ).all()

    return tasks