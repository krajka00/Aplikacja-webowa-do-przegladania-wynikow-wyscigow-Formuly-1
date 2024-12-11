import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import Header from './Header';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [races, setRaces] = useState([]);
  const [driverStandings, setDriverStandings] = useState([]);
  const [constructorStandings, setConstructorStandings] = useState([]);

  useEffect(() => {
    const verifyToken = async () => {
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        try {
          const response = await axios.post(
            'http://127.0.0.1:8000/api/token/verify/',
            { token: accessToken },
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );
          setIsLoggedIn(true);
          if (response.data.is_superuser) {
            localStorage.setItem('is_admin', 'true');
            setIsAdmin(true);
          } else {
            localStorage.setItem('is_admin', 'false');
            setIsAdmin(false);
          }
        } catch (error) {
          console.error('Token verification failed.', error);
          setIsLoggedIn(false);
          setIsAdmin(false);
          localStorage.removeItem('is_admin');
        }
      } else {
        setIsLoggedIn(false);
        setIsAdmin(false);
        localStorage.removeItem('is_admin');
      }
    };

    verifyToken();
  }, []);

  useEffect(() => {
    const fetchRaces = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/races/all/2023');
        setRaces(response.data);
      } catch (error) {
        console.error('Błąd podczas pobierania wyścigów', error);
      }
    };

    const fetchStandings = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/standings/current/');
        setDriverStandings(response.data.driver_standings);
        setConstructorStandings(response.data.constructor_standings);
      } catch (error) {
        console.error('Błąd podczas pobierania tabel', error);
      }
    };

    fetchRaces();
    fetchStandings();
  }, []);

  return (
    <div>
      <Header updateIsAdmin={(isAdmin) => setIsAdmin(isAdmin)} />
      <div className="races-container" style={{ paddingTop: '80px' }}>
        <h1>Lista Wyścigów 2023</h1>
        <div className="races-grid">
          {races.map((race) => (
            <Link to={`/races/${race.id}`} key={race.id} className="race-card-link">
              <div className="race-card">
                <h2>{race.official_name}</h2>
                <p>Data: {race.date}</p>
                <p>Runda: {race.round}</p>
              </div>
            </Link>
          ))}
        </div>

        <div className="tables-container">
          <div className="table-half">
            <h2>Aktualna Tabela Kierowców</h2>
            <table>
              <thead>
                <tr>
                  <th>Pozycja</th>
                  <th>Kierowca</th>
                  <th>Punkty</th>
                </tr>
              </thead>
              <tbody>
                {driverStandings.map((standing, index) => (
                  <tr key={index}>
                    <td>{standing.position}</td>
                    <td>
                      <Link to={`/drivers/${standing.driver_id}`} className="driver-link">
                        {standing.driver}
                      </Link>
                    </td>
                    <td>{standing.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="table-half">
            <h2>Aktualna Tabela Konstruktorów</h2>
            <table>
              <thead>
                <tr>
                  <th>Pozycja</th>
                  <th>Konstruktor</th>
                  <th>Punkty</th>
                </tr>
              </thead>
              <tbody>
                {constructorStandings.map((standing, index) => (
                  <tr key={index}>
                    <td>{standing.position}</td>
                    <td>
                      <Link to={`/constructors/${standing.constructor_id}`} className="constructor-link">
                        {standing.constructor}
                      </Link>
                    </td>
                    <td>{standing.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
