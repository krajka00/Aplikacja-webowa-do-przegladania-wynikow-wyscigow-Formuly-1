import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Header.css';

const Header = ({ updateIsAdmin }) => {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      setIsLoggedIn(true);
      const isSuperuser = localStorage.getItem('is_admin') === 'true';
      setIsAdmin(isSuperuser);
      if (updateIsAdmin) {
        updateIsAdmin(isSuperuser);
      }
    } else {
      setIsLoggedIn(false);
      setIsAdmin(false);
    }
  }, [updateIsAdmin]);

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
    } catch (error) {
      console.error('Logout failed', error);
    } finally {
      localStorage.clear();
      setIsLoggedIn(false);
      setIsAdmin(false);
      if (updateIsAdmin) {
        updateIsAdmin(false);
      }
      navigate('/');
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
        {isLoggedIn && isAdmin && (
          <Link to="/admin" className="admin-button">
            Zarządzaj
          </Link>
        )}
        {isLoggedIn ? (
          <button onClick={handleLogout} className="login-button1">
            Wyloguj
          </button>
        ) : (
          <Link to="/login" className="login-button1">
            Zaloguj
          </Link>
        )}
      </div>
    </header>
  );
};

export default Header;
