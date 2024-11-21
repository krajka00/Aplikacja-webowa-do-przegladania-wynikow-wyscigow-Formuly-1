import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import Header from './pages/Header';
import RacePage from './pages/RacePage';
import RegisterPage from './pages/RegisterPage';

function App() {
  return (
    <Router>
      <Header /> {/* Dodajemy Header na górze aplikacji */}
      <div className="app-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/races/:raceId" element={<RacePage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
