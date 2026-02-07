import axios from 'axios';

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface RegisterData {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

class AuthService {
  private static readonly BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  private static readonly AUTH_TOKEN_KEY = 'auth_token';

  // Helper method to check if running in browser
  static isBrowser(): boolean {
    return typeof window !== 'undefined';
  }

  // Register a new user
  static async register(userData: RegisterData): Promise<LoginResponse> {
    console.log(`Attempting to register user with email: ${userData.email}`);
    console.log(`Using API base URL: ${this.BASE_URL}`);
    
    try {
      const response = await axios.post(`${this.BASE_URL}/auth/register`, userData);
      console.log('Registration response received:', response.status);
      const { access_token, user } = response.data;

      // Store the token in localStorage (only in browser)
      if (this.isBrowser()) {
        localStorage.setItem(this.AUTH_TOKEN_KEY, access_token);
        console.log('Token stored in localStorage');
      }

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      console.error('Registration error details:', {
        message: error.message,
        response: error.response,
        request: error.request,
        config: error.config
      });
      
      let errorMessage = 'Registration failed';
      if (error.response) {
        errorMessage = error.response.data?.detail || `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'Network error: Unable to reach the server. Please check your connection.';
      } else {
        errorMessage = error.message || errorMessage;
      }
      
      throw new Error(errorMessage);
    }
  }

  // Login user
  static async login(email: string, password: string): Promise<LoginResponse> {
    console.log(`Attempting to login user with email: ${email}`);
    console.log(`Using API base URL: ${this.BASE_URL}`);
    
    try {
      const response = await axios.post(`${this.BASE_URL}/auth/login`, {
        email,
        password,
      }); // Send as JSON instead of form-encoded

      console.log('Login response received:', response.status);
      const { access_token, user } = response.data;

      // Store the token in localStorage (only in browser)
      if (this.isBrowser()) {
        localStorage.setItem(this.AUTH_TOKEN_KEY, access_token);
        console.log('Token stored in localStorage after login');
      }

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      console.error('Login error details:', {
        message: error.message,
        response: error.response,
        request: error.request,
        config: error.config
      });

      let errorMessage = 'Login failed';
      if (error.response) {
        errorMessage = error.response.data?.detail || `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'Network error: Unable to reach the server. Please check your connection.';
      } else {
        errorMessage = error.message || errorMessage;
      }

      throw new Error(errorMessage);
    }
  }

  // Logout user
  static logout(): void {
    if (this.isBrowser()) {
      localStorage.removeItem(this.AUTH_TOKEN_KEY);
    }
  }

  // Get current user token
  static getToken(): string | null {
    if (this.isBrowser()) {
      return localStorage.getItem(this.AUTH_TOKEN_KEY);
    }
    return null;
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // Get API instance with authentication
  static getApiInstance() {
    const instance = axios.create({
      baseURL: this.BASE_URL,
    });

    // Add auth token to requests
    instance.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Handle token expiration
    instance.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout();
        }
        return Promise.reject(error);
      }
    );

    return instance;
  }
}

export default AuthService;