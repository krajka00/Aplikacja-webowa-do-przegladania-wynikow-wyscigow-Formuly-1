import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import Header from './pages/Header';
import RacePage from './pages/RacePage';
import RegisterPage from './pages/RegisterPage';
import AdminPage from './pages/ManagementPanel'
import DriverPage from './pages/DriverPage';
import ConstructorPage from './pages/ConstructorPage';

function App() {
  return (
    <Router>
      <Header /> 
      <div className="app-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/races/:raceId" element={<RacePage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/drivers/:pk" element={<DriverPage />} />
          <Route path="/constructors/:pk" element={<ConstructorPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
