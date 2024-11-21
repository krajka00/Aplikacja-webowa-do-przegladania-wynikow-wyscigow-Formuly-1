import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './RegisterPage.css';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/api/register/', {
        username,
        email,
        password,
      });

      setMessage('Rejestracja zakończona sukcesem! Przekierowywanie do logowania...');
      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } catch (error) {
      setMessage('Rejestracja nie powiodła się. Sprawdź wprowadzone dane.');
    }
  };

  return (
    <div className="register-container">
      <form onSubmit={handleRegister} className="register-form">
        <h2>Rejestracja</h2>
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="register-button">Zarejestruj się</button>
      </form>

      {/* Wyświetlenie wiadomości o błędzie lub sukcesie poniżej formularza */}
      {message && <div className="register-message">{message}</div>}

      {/* Przycisk do przekierowania na stronę logowania */}
      <div className="redirect-login">
        <p>Masz już konto? <Link to="/login">Zaloguj się</Link></p>
      </div>
    </div>
  );
};

export default RegisterPage;
