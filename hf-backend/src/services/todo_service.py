from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User
from fastapi import HTTPException

class TodoService:
    @staticmethod
    def get_user_todos(session: Session, user_id: UUID) -> List[Todo]:
        statement = select(Todo).where(Todo.user_id == user_id)
        todos = session.exec(statement).all()
        return todos

    @staticmethod
    def create_todo(session: Session, todo_data: TodoCreate, user_id: UUID) -> Todo:
        db_todo = Todo(**todo_data.dict(), user_id=user_id)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def get_todo_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = session.exec(statement).first()
        return todo

    @staticmethod
    def update_todo(session: Session, todo_id: UUID, todo_update: TodoUpdate, user_id: UUID) -> Optional[Todo]:
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return None

        # Update the todo with provided values
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete_todo(session: Session, todo_id: UUID, user_id: UUID) -> bool:
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return False

        session.delete(db_todo)
        session.commit()
        return True

    @staticmethod
    def toggle_todo_completion(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return None

        db_todo.is_completed = not db_todo.is_completed
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo