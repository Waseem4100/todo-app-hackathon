'use client';

import React, { useState } from 'react';
import { CreateTodoData, TodoApiService } from '../services/api';

interface TodoFormProps {
  onAddTodo: (todo: any) => void;
}

const TodoForm: React.FC<TodoFormProps> = ({ onAddTodo }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      alert('Please enter a title for the todo');
      return;
    }

    setIsLoading(true);

    try {
      const newTodo = await TodoApiService.createTodo({
        title: title.trim(),
        description: description.trim(),
      });

      onAddTodo(newTodo);
      setTitle('');
      setDescription('');
    } catch (error) {
      console.error('Failed to create todo:', error);
      alert('Failed to create todo');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <div className="form-group">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter todo title..."
          className="todo-input"
          disabled={isLoading}
        />
      </div>
      <div className="form-group">
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter description (optional)..."
          className="todo-textarea"
          rows={3}
          disabled={isLoading}
        />
      </div>
      <button type="submit" className="add-btn" disabled={isLoading}>
        {isLoading ? 'Adding...' : 'Add Todo'}
      </button>
    </form>
  );
};

export default TodoForm;