from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from uuid import UUID
from src.database.database import get_session
from src.models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from src.models.user import User
from src.api.deps import get_current_user
from src.services.todo_service import TodoService

router = APIRouter()

@router.get("/", response_model=List[TodoRead])
def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all todos for the current user
    """
    todos = TodoService.get_user_todos(session, current_user.id)
    return todos

@router.post("/", response_model=TodoRead, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the current user
    """
    todo = TodoService.create_todo(session, todo_data, current_user.id)
    return todo

@router.get("/{id}", response_model=TodoRead)
def get_todo(
    id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID
    """
    todo = TodoService.get_todo_by_id(session, id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{id}", response_model=TodoRead)
def update_todo(
    id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo
    """
    todo = TodoService.update_todo(session, id, todo_update, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{id}")
def delete_todo(
    id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo
    """
    success = TodoService.delete_todo(session, id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

@router.patch("/{id}/toggle-complete", response_model=TodoRead)
def toggle_todo_complete(
    id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific todo
    """
    todo = TodoService.toggle_todo_completion(session, id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo