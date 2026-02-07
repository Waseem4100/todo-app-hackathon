import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import dynamic from 'next/dynamic';
import TodoList from '../components/TodoList';
import AuthService from '../services/auth';

// Dynamically import Layout with no SSR to avoid localStorage issues
const DynamicLayout = dynamic(() => import('../components/Layout'), {
  ssr: false,
  loading: () => (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <a href="/" className="nav-brand">
            Todo App
          </a>
          <div className="nav-links">
            <a href="/login" className="nav-link">
              Login
            </a>
            <a href="/signup" className="nav-link">
              Sign Up
            </a>
          </div>
        </div>
      </nav>
      <main className="main-content">
        <div>Loading...</div>
      </main>
      <footer className="footer">
        <div className="footer-container">
          <p>&copy; 2026 Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  ),
});

const TodosPage: React.FC = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    if (AuthService.isBrowser() && !AuthService.isAuthenticated()) {
      router.push('/login');
    } else {
      setLoading(false);
    }
  }, [router]);

  if (loading) {
    return (
      <DynamicLayout>
        <div className="page-container">
          <div>Loading...</div>
        </div>
      </DynamicLayout>
    );
  }

  // If not authenticated, don't render the content
  if (AuthService.isBrowser() && !AuthService.isAuthenticated()) {
    return <div>Redirecting...</div>;
  }

  return (
    <DynamicLayout>
      <div className="page-container">
        <TodoList />
      </div>
    </DynamicLayout>
  );
};

export default TodosPage;