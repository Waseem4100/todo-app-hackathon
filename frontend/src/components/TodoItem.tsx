'use client';

import React from 'react';
import { Todo, TodoApiService } from '../services/api';

interface TodoItemProps {
  todo: Todo;
  onToggle: (updatedTodo: Todo) => void;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  const handleToggle = async () => {
    try {
      const updatedTodo = await TodoApiService.toggleTodoCompletion(todo.id);
      onToggle(updatedTodo);
    } catch (error) {
      console.error('Failed to toggle todo:', error);
      alert('Failed to update todo status');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await TodoApiService.deleteTodo(todo.id);
        onDelete(todo.id);
      } catch (error) {
        console.error('Failed to delete todo:', error);
        alert('Failed to delete todo');
      }
    }
  };

  return (
    <div className={`todo-item ${todo.is_completed ? 'completed' : ''}`}>
      <div className="todo-content">
        <input
          type="checkbox"
          checked={todo.is_completed}
          onChange={handleToggle}
          className="todo-checkbox"
        />
        <div className="todo-text">
          <h3>{todo.title}</h3>
          {todo.description && <p>{todo.description}</p>}
          <small>Created: {new Date(todo.created_at).toLocaleString()}</small>
        </div>
      </div>
      <button onClick={handleDelete} className="delete-btn">
        Delete
      </button>
    </div>
  );
};

export default TodoItem;