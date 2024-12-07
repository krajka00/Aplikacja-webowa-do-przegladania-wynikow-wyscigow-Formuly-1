import React, { useState } from 'react';
import api from '../services/api';
import { useNavigate, Link } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('token/', { username, password });

      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);

      setMessage('Logowanie zakończone sukcesem! Przekierowywanie...');
      setTimeout(() => {
        navigate('/');
      }, 1500);
    } catch (error) {
      setMessage('Błędne dane logowania. Spróbuj ponownie.');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <h2>Login</h2>
        <div className="form-group">
          <label>Login:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Hasło:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="login-button">Log In</button>
      </form>

      {/* Wyświetlenie wiadomości o błędzie lub sukcesie poniżej formularza */}
      {message && <div className="login-message">{message}</div>}

      {/* Przycisk do przekierowania na stronę rejestracji */}
      <div className="redirect-register">
        <p>Nie masz konta? <Link to="/register">Zarejestruj się</Link></p>
      </div>
    </div>
  );
};

export default LoginPage;
