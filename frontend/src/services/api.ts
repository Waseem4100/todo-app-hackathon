import axios from 'axios';
import AuthService from './auth';

interface Todo {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface CreateTodoData {
  title: string;
  description?: string;
  is_completed?: boolean;
}

interface UpdateTodoData {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

class TodoApiService {
  private static readonly BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  // Helper method to check if running in browser
  private static isBrowser(): boolean {
    return typeof window !== 'undefined';
  }

  // Get axios instance with auth header
  private static getAxiosInstance() {
    const instance = axios.create({
      baseURL: this.BASE_URL,
    });

    // Only add auth token if in browser and user is authenticated
    if (this.isBrowser()) {
      const token = AuthService.getToken();
      if (token) {
        instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }
    }

    return instance;
  }

  // Get all todos for the current user
  static async getTodos(): Promise<Todo[]> {
    try {
      const instance = this.getAxiosInstance();
      const response = await instance.get('/todos');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch todos');
    }
  }

  // Create a new todo
  static async createTodo(todoData: CreateTodoData): Promise<Todo> {
    try {
      const instance = this.getAxiosInstance();
      const response = await instance.post('/todos', todoData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to create todo');
    }
  }

  // Get a specific todo by ID
  static async getTodoById(id: string): Promise<Todo> {
    try {
      const instance = this.getAxiosInstance();
      const response = await instance.get(`/todos/${id}`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch todo');
    }
  }

  // Update a specific todo
  static async updateTodo(id: string, todoData: UpdateTodoData): Promise<Todo> {
    try {
      const instance = this.getAxiosInstance();
      const response = await instance.put(`/todos/${id}`, todoData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to update todo');
    }
  }

  // Delete a specific todo
  static async deleteTodo(id: string): Promise<void> {
    try {
      const instance = this.getAxiosInstance();
      await instance.delete(`/todos/${id}`);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to delete todo');
    }
  }

  // Toggle todo completion status
  static async toggleTodoCompletion(id: string): Promise<Todo> {
    try {
      const instance = this.getAxiosInstance();
      const response = await instance.patch(`/todos/${id}/toggle-complete`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to toggle todo completion');
    }
  }
}

export { TodoApiService, type Todo, type CreateTodoData, type UpdateTodoData };