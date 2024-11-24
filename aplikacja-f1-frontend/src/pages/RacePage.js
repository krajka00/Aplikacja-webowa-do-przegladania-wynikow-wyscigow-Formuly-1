import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Header from './Header';
import './RacePage.css';

const RacePage = () => {
  const { raceId } = useParams();
  const [raceDetails, setRaceDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeSection, setActiveSection] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const fetchRaceDetails = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/races/${raceId}/`);
        setRaceDetails(response.data);
      } catch (error) {
        setError('Nie udało się pobrać szczegółów wyścigu.');
      } finally {
        setLoading(false);
      }
    };
    const fetchComments = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/races/${raceId}/comments/`);
        setComments(response.data);
      } catch (error) {
        console.error('Błąd podczas pobierania komentarzy', error);
      }
    };
    

    fetchRaceDetails();
    fetchComments();
  }, [raceId]);

  if (loading) {
    return <div>Ładowanie szczegółów wyścigu...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  const toggleSection = (section) => {
    if (activeSection === section) {
      setActiveSection(null);
    } else {
      setActiveSection(section);
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
  try {
    const accessToken = localStorage.getItem('access_token');
    console.log('Access Token:', accessToken);
    const response = await axios.post(
      `http://127.0.0.1:8000/api/races/${raceId}/comments/create/`,
      {
        content: newComment,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );
    setComments([...comments, response.data]);
    setNewComment('');
  } catch (error) {
    console.error('Nie udało się dodać komentarza', error);
    console.error('Response status:', error.response?.status);
    console.error('Response data:', error.response?.data);
  }
  };
  

  const renderSectionContent = () => {
    switch (activeSection) {
      case 'results':
        return raceDetails.results && raceDetails.results.length > 0 ? (
          <div className="section">
            <h2>Wyniki Wyścigu</h2>
            <table>
              <thead>
                <tr>
                  <th>Pozycja</th>
                  <th>Kierowca</th>
                  <th>Konstruktor</th>
                  <th>Punkty</th>
                  <th>Okrążenia</th>
                  <th>Czas</th>
                  <th>Strata do lidera</th>
                </tr>
              </thead>
              <tbody>
                {sortResults(raceDetails.results).map((result, index) => (
                  <tr key={index}>
                    <td>{getPositionLabel(result.position)}</td>
                    <td>{result.driver}</td>
                    <td>{result.constructor}</td>
                    <td>{result.points}</td>
                    <td>{result.laps}</td>
                    <td>{result.time}</td>
                    <td>{result.gap}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null;

      case 'qualifying':
        return raceDetails.qualifying_results && raceDetails.qualifying_results.length > 0 ? (
          <div className="section">
            <h2>Wyniki Kwalifikacji</h2>
            <table>
              <thead>
                <tr>
                  <th>Pozycja</th>
                  <th>Kierowca</th>
                  <th>Konstruktor</th>
                  <th>Q1</th>
                  <th>Q2</th>
                  <th>Q3</th>
                  <th>Strata do lidera</th>
                  <th>Okrążenia</th>
                </tr>
              </thead>
              <tbody>
                {sortResults(raceDetails.qualifying_results).map((qualifying, index) => (
                  <tr key={index}>
                    <td>{getPositionLabel(qualifying.position)}</td>
                    <td>{qualifying.driver}</td>
                    <td>{qualifying.constructor}</td>
                    <td>{qualifying.q1_time}</td>
                    <td>{qualifying.q2_time}</td>
                    <td>{qualifying.q3_time}</td>
                    <td>{qualifying.gap}</td>
                    <td>{qualifying.laps}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null;

      case 'sprint_qualifying':
        return raceDetails.sprint_qualifying_results && raceDetails.sprint_qualifying_results.length > 0 ? (
          <div className="section">
            <h2>Wyniki Kwalifikacji Sprintu</h2>
            <table>
              <thead>
                <tr>
                  <th>Pozycja</th>
                  <th>Kierowca</th>
                  <th>Konstruktor</th>
                  <th>Q1</th>
                  <th>Q2</th>
                  <th>Q3</th>
                  <th>Strata do lidera</th>
                  <th>Okrążenia</th>
                </tr>
              </thead>
              <tbody>
                {sortResults(raceDetails.sprint_qualifying_results).map((qualifying, index) => (
                  <tr key={index}>
                    <td>{getPositionLabel(qualifying.position)}</td>
                    <td>{qualifying.driver}</td>
                    <td>{qualifying.constructor}</td>
                    <td>{qualifying.q1_time}</td>
                    <td>{qualifying.q2_time}</td>
                    <td>{qualifying.q3_time}</td>
                    <td>{qualifying.gap}</td>
                    <td>{qualifying.laps}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null;

      case 'sprint':
        return raceDetails.sprint_results && raceDetails.sprint_results.length > 0 ? (
          <div className="section">
            <h2>Wyniki Sprintu</h2>
            <table>
              <thead>
                <tr>
                  <th>Pozycja</th>
                  <th>Kierowca</th>
                  <th>Konstruktor</th>
                  <th>Czas</th>
                  <th>Kara</th>
                  <th>Strata do lidera</th>
                  <th>Interwał</th>               
                  <th>Punkty</th>
                </tr>
              </thead>
              <tbody>
                {sortResults(raceDetails.sprint_results).map((sprint, index) => (
                  <tr key={index}>
                    <td>{getPositionLabel(sprint.position)}</td>
                    <td>{sprint.driver}</td>
                    <td>{sprint.constructor}</td>
                    <td>{sprint.time}</td>
                    <td>{sprint.time_penalty}</td>
                    <td>{sprint.gap}</td>
                    <td>{sprint.interval}</td>
                    <td>{sprint.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null;

        case 'fastest_laps':
          return raceDetails.fastest_laps && raceDetails.fastest_laps.length > 0 ? (
            <div className="section">
              <h2>Najszybsze Okrążenia</h2>
              <table>
                <thead>
                  <tr>
                    <th>Kierowca</th>
                    <th>Okrążenie</th>
                    <th>Czas Okrążenia</th>
                    <th>Strata</th>
                    <th>Interwał</th>
                  </tr>
                </thead>
                <tbody>
                {raceDetails.fastest_laps
                  .map((lap) => ({
                    ...lap,
                    gapValue: lap.gap && typeof lap.gap === 'string' ? parseFloat(lap.gap.replace('+', '')) : 0
                  }))
                  .sort((a, b) => a.gapValue - b.gapValue)
                  .map((lap, index) => (
                    <tr key={index}>
                      <td>{lap.driver}</td>
                      <td>{lap.lap}</td>
                      <td>{lap.lap_time}</td>
                      <td>{lap.gap}</td>
                      <td>{lap.interval}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : null;

      default:
        if (activeSection && activeSection.startsWith('practice')) {
          const sessionNumber = parseInt(activeSection.split('-')[1]);
          const practiceSessions = raceDetails.practice_sessions.filter(
            session => session.session_number === sessionNumber
          );

          return practiceSessions.length > 0 ? (
            <div className="section">
              <h2>Trening {sessionNumber}</h2>
              <table>
                <thead>
                  <tr>
                    <th>Pozycja</th>
                    <th>Kierowca</th>
                    <th>Konstruktor</th>
                    <th>Czas</th>
                    <th>Okrążenia</th>
                  </tr>
                </thead>
                <tbody>
                  {sortResults(practiceSessions).map((session, index) => (
                    <tr key={index}>
                      <td>{getPositionLabel(session.position)}</td>
                      <td>{session.driver}</td>
                      <td>{session.constructor}</td>
                      <td>{session.time}</td>
                      <td>{session.laps}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : null;
        }

        return null;
    }
  };

  const getPositionLabel = (position) => {
    if (position === 0) {
      return 'DNF';
    } else if (position === 99) {
      return 'DNS';
    } else if (position === 999) {
      return 'DSQ';
    } else if (position > 20) {
      return 'DNF';
    } else {
      return position;
    }
  };

  const sortResults = (results) => {
    return results.sort((a, b) => {
      if (a.position === 0 || a.position > 20) {
        return 1;
      }
      if (b.position === 0 || b.position > 20) {
        return -1;
      }
      return a.position - b.position;
    });
  };

  return (
    <div>
      <Header />
      <div className="race-details-container" style={{ paddingTop: '80px' }}>
        <div className="race-header">
          <h1>Szczegóły Wyścigu: {raceDetails.race_details.official_name}</h1>
          <p><strong>Data:</strong> {raceDetails.race_details.date}</p>
          <p><strong>Runda:</strong> {raceDetails.race_details.round}</p>
          <p><strong>Sezon:</strong> {raceDetails.race_details.season}</p>
          <p><strong>Tor:</strong> {raceDetails.race_details.circuit}</p>
          <p><strong>Dystans:</strong> {raceDetails.race_details.distance} km</p>
        </div>

        {/* Kafelki do przełączania sekcji */}
        <div className="stats-menu">
          {raceDetails.results && raceDetails.results.length > 0 && (
            <div className="stat-card" onClick={() => toggleSection('results')}>
              Wyniki Wyścigu
            </div>
          )}
          {raceDetails.fastest_laps && raceDetails.fastest_laps.length > 0 && (
            <div className="stat-card" onClick={() => toggleSection('fastest_laps')}>
              Najszybsze Okrążenia
            </div>
          )}
          {raceDetails.qualifying_results && raceDetails.qualifying_results.length > 0 && (
            <div className="stat-card" onClick={() => toggleSection('qualifying')}>
              Wyniki Kwalifikacji
            </div>
          )}
          {raceDetails.sprint_qualifying_results && raceDetails.sprint_qualifying_results.length > 0 && (
            <div className="stat-card" onClick={() => toggleSection('sprint_qualifying')}>
              Wyniki Kwalifikacji Sprintu
            </div>
          )}
          {raceDetails.sprint_results && raceDetails.sprint_results.length > 0 && (
            <div className="stat-card" onClick={() => toggleSection('sprint')}>
              Wyniki Sprintu
            </div>
          )}
          {raceDetails.practice_sessions && raceDetails.practice_sessions.length > 0 &&
            [...new Set(raceDetails.practice_sessions.map(session => session.session_number))].map(sessionNumber => (
              <div
                key={sessionNumber}
                className="stat-card"
                onClick={() => toggleSection(`practice-${sessionNumber}`)}
              >
                Trening {sessionNumber}
              </div>
            ))}
        </div>

        {/* Renderowanie zawartości sekcji */}
        {renderSectionContent()}

        <div className="comments-section">
          <h2>Komentarze</h2>
          <div className="comments-list">
            {comments.length > 0 ? (
              comments.map((comment, index) => (
                <div key={index} className="comment">
                  <p><strong>{comment.username}:</strong> {comment.content}</p>
                </div>
              ))
            ) : (
              <p>Brak komentarzy. Bądź pierwszy, który doda komentarz!</p>
            )}
          </div>

          {localStorage.getItem('access_token') && (
            <form onSubmit={handleCommentSubmit} className="comment-form">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Dodaj swój komentarz..."
                required
              />
              <button type="submit">Dodaj komentarz</button>
            </form>
          )}
        </div>

      </div>
    </div>
  );
};

export default RacePage;
