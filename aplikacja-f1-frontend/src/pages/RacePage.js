import React, { useEffect, useState } from 'react';
import api from '../services/api';
import CommentSection from '../components/CommentSection';
import { useParams } from 'react-router-dom';

const RacePage = () => {
  const { raceId } = useParams();
  const [raceDetails, setRaceDetails] = useState(null);
  const isAdmin = localStorage.getItem('is_admin') === 'true';

  useEffect(() => {
    const fetchRaceDetails = async () => {
      try {
        const response = await api.get(`races/${raceId}/`);
        setRaceDetails(response.data);
      } catch (error) {
        console.error('Błąd podczas pobierania szczegółów wyścigu', error);
      }
    };

    fetchRaceDetails();
  }, [raceId]);

  if (!raceDetails) return <div>Ładowanie...</div>;

  return (
    <div>
      <h1>{raceDetails.race_details.official_name}</h1>

      {/* Wyświetlanie szczegółów wyścigu */}
      <div>
        <p>Data: {raceDetails.race_details.date}</p>
        <p>Obiekt: {raceDetails.race_details.circuit}</p>
        {/* Dodaj inne szczegóły wyścigu */}
      </div>

      {/* Sekcja komentarzy - dostępna dla zalogowanych użytkowników */}
      <CommentSection raceId={raceId} />

      {/* Przyciski administracyjne - dostępne tylko dla administratora */}
      {isAdmin && (
        <div>
          <button onClick={() => handleEditRace(raceId)}>Edytuj wyścig</button>
          <button onClick={() => handleDeleteRace(raceId)}>Usuń wyścig</button>
        </div>
      )}
    </div>
  );
};

const handleEditRace = (raceId) => {
  console.log('Edytowanie wyścigu', raceId);
};

const handleDeleteRace = async (raceId) => {
  try {
    await api.delete(`races/${raceId}/`);
    console.log('Wyścig usunięty');
  } catch (error) {
    console.error('Błąd podczas usuwania wyścigu', error);
  }
};

export default RacePage;
