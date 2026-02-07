import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import AuthService from '../services/auth';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (AuthService.isBrowser()) {
      setIsLoggedIn(AuthService.isAuthenticated());
    }
    setLoading(false);
  }, []);

  const handleLogout = () => {
    AuthService.logout();
    router.push('/login'); // Use router instead of window.location for better Next.js integration
  };

  if (loading) {
    return (
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
    );
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link href="/" className="nav-brand">
            Todo App
          </Link>

          <div className="nav-links">
            {isLoggedIn ? (
              <>
                <Link href="/todos" className="nav-link">
                  My Todos
                </Link>
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="nav-link">
                  Login
                </Link>
                <Link href="/signup" className="nav-link">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <main className="main-content">
        {children}
      </main>

      <footer className="footer">
        <div className="footer-container">
          <p>&copy; 2026 Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;