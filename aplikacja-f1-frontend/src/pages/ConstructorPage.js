import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Header from './Header';
import './ConstructorPage.css';

const ConstructorPage = () => {
  const { pk } = useParams();
  const [constructorData, setConstructorData] = useState(null);
  const [constructorStandings, setConstructorStandings] = useState([]);
  const [raceData, setRaceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [countryData, setCountryData] = useState({});
  const [pointsDifferences, setPointsDifferences] = useState([]);

  useEffect(() => {
    const fetchConstructorData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/constructor/${pk}/`);
        setConstructorData(response.data);

        const countryResponse = await axios.get(`http://127.0.0.1:8000/api/country/${response.data.country}/`);
        setCountryData(countryResponse.data);

        const standingsResponse = await axios.get(`http://127.0.0.1:8000/api/constructor_standing/all/${pk}/`);
        setConstructorStandings(standingsResponse.data);

        const differences = standingsResponse.data.map((standing, index, array) => {
          if (index === 0) return 0;
          return standing.points - array[index - 1].points;
        });
        setPointsDifferences(differences);

        const currentYear = new Date().getFullYear();
        const raceResponse = await axios.get(`http://127.0.0.1:8000/api/races/all/2023/`);
        setRaceData(raceResponse.data);
      } catch (error) {
        setError('Nie udało się pobrać danych konstruktora lub jego wyników.');
      } finally {
        setLoading(false);
      }
    };

    fetchConstructorData();
  }, [pk]);

  if (loading) {
    return <div className="loading">Ładowanie danych konstruktora...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div>
      <Header />
      <div className="constructor-details-container">
        <h1>Szczegóły Konstruktor: {constructorData.name}</h1>
        <div className="constructor-info">
          <p><strong>Pełna nazwa:</strong> {constructorData.full_name}</p>
          <p><strong>Kraj:</strong> {countryData.name || 'Brak danych'}</p>
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
              {constructorStandings.map((standing, index) => {
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

export default ConstructorPage;