import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Header.css';

const Header = () => {
  const navigate = useNavigate();
  const isLoggedIn = Boolean(localStorage.getItem('access_token'));

  const handleLogout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        await axios.post(
          'http://127.0.0.1:8000/api/logout/',
          { refresh: refreshToken },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }
        );
      }

      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');

      navigate('/');
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  return (
    <header className="header">
      <div className="banner">
        <Link to="/" className="banner-link">
          <h1>Formuła 1 - Wyniki Wyścigów</h1>
        </Link>
      </div>
      <div className="login-link">
        {isLoggedIn ? (
          <button onClick={handleLogout} className="login-button">
            Wyloguj
          </button>
        ) : (
          <Link to="/login" className="login-button">
            Zaloguj
          </Link>
        )}
      </div>
    </header>
  );
};

export default Header;
