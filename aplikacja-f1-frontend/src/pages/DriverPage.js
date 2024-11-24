import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Header from './Header';
import './DriverPage.css';

const DriverPage = () => {
  const { pk } = useParams();
  const [driverData, setDriverData] = useState(null);
  const [countryData, setCountryData] = useState({});
  const [driverStandings, setDriverStandings] = useState([]);
  const [raceData, setRaceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pointsDifferences, setPointsDifferences] = useState([]);

  useEffect(() => {
    const fetchDriverData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/driver/${pk}/`);
        setDriverData(response.data);
        const countryResponse = await axios.get(`http://127.0.0.1:8000/api/country/${response.data.country_of_birth}/`);
        setCountryData(countryResponse.data);

        const standingsResponse = await axios.get(`http://127.0.0.1:8000/api/driver_standing/all/${pk}/`);
        setDriverStandings(standingsResponse.data);

        const differences = standingsResponse.data.map((standing, index, array) => {
          if (index === 0) return 0;
          return standing.points - array[index - 1].points;
        });
        setPointsDifferences(differences);

        const currentYear = new Date().getFullYear();
        const raceResponse = await axios.get(`http://127.0.0.1:8000/api/races/all/2023/`);
        setRaceData(raceResponse.data);
      } catch (error) {
        setError('Nie udało się pobrać danych kierowcy, kraju lub wyników.');
      } finally {
        setLoading(false);
      }
    };

    fetchDriverData();
  }, [pk]);

  if (loading) {
    return <div>Ładowanie danych kierowcy...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <Header />
      <div className="driver-details-container" style={{ paddingTop: '80px' }}>
        <h1>Szczegóły Kierowcy: {driverData.first_name} {driverData.last_name}</h1>
        <div className="driver-info">
          <p><strong>Numer stały:</strong> {driverData.permanent_number || 'Brak'}</p>
          <p><strong>Skrót:</strong> {driverData.abbreviation}</p>
          <p><strong>Płeć:</strong> {driverData.gender}</p>
          <p><strong>Data urodzenia:</strong> {driverData.date_of_birth}</p>
          {driverData.date_of_death && (
            <p><strong>Data śmierci:</strong> {driverData.date_of_death}</p>
          )}
          <p><strong>Miejsce urodzenia:</strong> {driverData.place_of_birth}</p>
          <p><strong>Kraj urodzenia:</strong> {countryData.name || 'Brak danych'}</p>
          <p><strong>Narodowość:</strong> {countryData.demonym || 'Brak danych'}</p>
        </div>
        <div className="standings-container">
          <h2>Zmiany punktów w wynikach po weekendzie wyscigowym</h2>
          <table className="standings-table">
            <thead>
              <tr>
                <th>Wyścig</th>
                <th>Data</th>
                <th>Pozycja</th>
                <th>Punkty</th>
                <th>Różnica</th>
              </tr>
            </thead>
            <tbody>
              {driverStandings.map((standing, index) => {
                const race = raceData.find(race => race.id === standing.race);
                return (
                  <tr key={index}>
                    <td>{race ? race.official_name : 'N/A'}</td>
                    <td>{race ? race.date : 'N/A'}</td>
                    <td>{standing.position}</td>
                    <td>{standing.points}</td>
                    <td>{pointsDifferences[index]}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DriverPage;