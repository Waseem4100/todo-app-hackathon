import React from 'react';
import dynamic from 'next/dynamic';

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

const Custom500 = () => {
  return (
    <DynamicLayout>
      <div className="error-page">
        <h1>500 - Internal Server Error</h1>
        <p>Sorry, something went wrong. Please try again later.</p>
        <a href="/">Go back home</a>
      </div>
    </DynamicLayout>
  );
};

export default Custom500;