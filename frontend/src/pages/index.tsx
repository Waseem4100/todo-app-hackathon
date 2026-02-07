import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import AuthService from '../services/auth';

// Dynamically import Layout with no SSR to avoid localStorage issues
const DynamicLayout = dynamic(() => import('../components/Layout'), {
  ssr: false,
  loading: () => (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link href="/" className="nav-brand">
            Todo App
          </Link>
          <div className="nav-links">
            <Link href="/login" className="nav-link">
              Login
            </Link>
            <Link href="/signup" className="nav-link">
              Sign Up
            </Link>
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

const HomePage: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (AuthService.isBrowser()) {
      setIsLoggedIn(AuthService.isAuthenticated());
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <DynamicLayout>{null}</DynamicLayout>;
  }

  return (
    <DynamicLayout>
      <div className="home-page">
        <div className="hero-section">
          <h1>Welcome to Todo App</h1>
          <p>Manage your tasks efficiently and boost your productivity</p>

          {isLoggedIn ? (
            <Link href="/todos" className="cta-button">
              View My Todos
            </Link>
          ) : (
            <div className="auth-options">
              <Link href="/signup" className="cta-button">
                Get Started
              </Link>
              <span className="or-separator">or</span>
              <Link href="/login" className="secondary-button">
                Log In
              </Link>
            </div>
          )}
        </div>

        <div className="features-section">
          <div className="feature-card">
            <h3>Create Tasks</h3>
            <p>Easily add new tasks with titles and descriptions</p>
          </div>
          <div className="feature-card">
            <h3>Track Progress</h3>
            <p>Mark tasks as complete to track your progress</p>
          </div>
          <div className="feature-card">
            <h3>Stay Organized</h3>
            <p>Keep all your tasks organized in one place</p>
          </div>
        </div>
      </div>
    </DynamicLayout>
  );
};

export default HomePage;