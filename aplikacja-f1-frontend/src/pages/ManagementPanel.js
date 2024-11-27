import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Header from './Header';
import './ManagementPanel.css';

const ManagementPanel = () => {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedItem, setSelectedItem] = useState('');
  const [dataList, setDataList] = useState([]);
  const [formData, setFormData] = useState({});
  const [fieldDefinitions, setFieldDefinitions] = useState([]);
  const [relatedData, setRelatedData] = useState({});

  const categories = [
    'continent', 'country', 'constructor', 'circuit', 'driver', 'constructor_standing', 'driver_standing',
    'race', 'race_result', 'fastest_lap', 'pit_stop', 'qualifying_result', 'sprint_qualifying_result',
    'sprint_race_result', 'practice_session'
  ];

  useEffect(() => {
    const verifyToken = async () => {
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        try {
          await axios.post(
            'http://127.0.0.1:8000/api/token/verify/',
            { token: accessToken },
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );
          setIsLoggedIn(true);
        } catch (error) {
          console.error('Token verification failed.', error);
          setIsLoggedIn(false);
        }
      } else {
        setIsLoggedIn(false);
      }
    };

    verifyToken();
  }, []);

  const handleCategoryChange = (e) => {
    const category = e.target.value;
    setSelectedCategory(category);
    setSelectedItem('');
    setFormData({});
    setFieldDefinitions([]);
    fetchData(category);
    determineFields(category);
    fetchRelatedData(category);
  };

  const handleItemChange = (e) => {
    const itemId = e.target.value;
    setSelectedItem(itemId);
    if (itemId) {
      const selectedItemData = dataList.find((item) => item.id.toString() === itemId);
      setFormData(selectedItemData);
    } else {
      setFormData({});
    }
  };

  const fetchData = async (category) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/${category}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setDataList(response.data);
    } catch (error) {
      console.error(`Error fetching ${category}`, error);
    }
  };

  const determineFields = (category) => {
    const fields = {
      continent: ['code', 'name', 'demonym'],
      country: ['name', 'alpha2_code', 'alpha3_code', 'demonym', 'continent'],
      constructor: ['name', 'full_name', 'country'],
      circuit: ['name', 'full_name', 'circuit_type', 'place_name', 'country', 'latitude', 'longitude'],
      driver: ['first_name', 'last_name', 'abbreviation', 'permanent_number', 'gender', 'date_of_birth', 'date_of_death', 'place_of_birth', 'country_of_birth', 'nationality'],
      tyre_manufacturer: ['name', 'country'],
      constructor_standing: ['constructor', 'race', 'position', 'points'],
      driver_standing: ['driver', 'race', 'position', 'points'],
      race: ['official_name', 'season', 'round', 'date', 'circuit', 'laps', 'distance', 'course_length'],
      fastest_lap: ['race', 'driver', 'constructor', 'lap', 'lap_time', 'gap', 'interval'],
      pit_stop: ['race', 'driver', 'stop_number', 'lap', 'duration', 'time_of_day'],
      qualifying_result: ['race', 'driver', 'constructor', 'position', 'q1_time', 'q2_time', 'q3_time', 'laps', 'gap', 'interval'],
      sprint_qualifying_result: ['race', 'driver', 'constructor', 'position', 'q1_time', 'q2_time', 'q3_time', 'laps', 'gap', 'interval'],
      sprint_race_result: ['race', 'driver', 'constructor', 'position', 'laps', 'time', 'time_penalty', 'gap', 'interval', 'reason_retired', 'points'],
      practice_session: ['race', 'session_number', 'driver', 'constructor', 'position', 'laps', 'time', 'gap', 'interval'],
      race_result: ['race', 'driver', 'constructor', 'position', 'points', 'laps', 'time', 'time_penalty', 'gap', 'interval', 'reason_retired'],
    };
    setFieldDefinitions(fields[category] || []);
  };

  const fetchRelatedData = async (category) => {
    const relatedFields = {
      country: 'continent',
      constructor: 'country',
      circuit: 'country',
      driver: ['country_of_birth', 'nationality'],
      race: 'circuit',
      constructor_standing: ['constructor', 'race'],
      driver_standing: ['driver', 'race'],
      fastest_lap: ['race', 'driver', 'constructor'],
      pit_stop: ['race', 'driver'],
      qualifying_result: ['race', 'driver', 'constructor'],
      sprint_qualifying_result: ['race', 'driver', 'constructor'],
      sprint_race_result: ['race', 'driver', 'constructor'],
      practice_session: ['race', 'driver', 'constructor'],
      race_result: ['race', 'driver', 'constructor'],
    };

    const related = relatedFields[category];
    if (related) {
      try {
        if (Array.isArray(related)) {
          const relatedDataPromises = related.map(async (field) => {
            const response = await axios.get(`http://127.0.0.1:8000/api/${field}/`, {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
              }
            });
            return { [field]: response.data };
          });
          const relatedDataArray = await Promise.all(relatedDataPromises);
          const combinedRelatedData = relatedDataArray.reduce((acc, curr) => ({ ...acc, ...curr }), {});
          setRelatedData(combinedRelatedData);
        } else {
          const response = await axios.get(`http://127.0.0.1:8000/api/${related}/`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          });
          setRelatedData({ [related]: Array.isArray(response.data) ? response.data : [] });
        }
      } catch (error) {
        console.error('Error fetching related data', error);
      }
    } else {
      setRelatedData({});
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (formData.id) {
        await axios.put(`http://127.0.0.1:8000/api/${selectedCategory}/update/${formData.id}/`, formData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });
      } else {
        await axios.post(`http://127.0.0.1:8000/api/${selectedCategory}/create/`, formData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });
      }
      fetchData(selectedCategory);
      setFormData({});
    } catch (error) {
      console.error('Error submitting form data', error);
    }
  };

  return (
    <div>
      <Header isLoggedIn={isLoggedIn} />
      <div className="management-panel-container">
        <h1>Panel Zarządzania Danymi Wyścigów</h1>
        <div className="category-selector">
          <label>Wybierz kategorię: </label>
          <select value={selectedCategory} onChange={handleCategoryChange}>
            <option value="">-- Wybierz --</option>
            {categories.map((category) => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>

        {selectedCategory && (
          <div className="item-selector" style={{ minHeight: '50px' }}>
            <label>Wybierz element do edycji: </label>
            <select value={selectedItem} onChange={handleItemChange} style={{ width: '100%', padding: '10px', fontSize: '16px' }}>
              <option value="">-- Wybierz --</option>
              {dataList.map((item) => (
                <option key={item.id} value={item.id}>
                  {selectedCategory === 'constructor_standing' ? 
                    `Wyścig: ${relatedData.race?.find(r => r.id === item.race)?.official_name || item.race}, Konstruktor: ${relatedData.constructor?.find(c => c.id === item.constructor)?.name || item.constructor}` :
                   selectedCategory === 'driver_standing' ?
                    `Wyścig: ${relatedData.race?.find(r => r.id === item.race)?.official_name || item.race}, Kierowca: ${relatedData.driver?.find(d => d.id === item.driver)?.first_name + ' ' + relatedData.driver?.find(d => d.id === item.driver)?.last_name || item.driver}` :
                   ['pit_stop', 'qualifying_result', 'sprint_qualifying_result', 'sprint_race_result', 'practice_session', 'race_result', 'fastest_lap'].includes(selectedCategory) ?
                    `Wyścig: ${relatedData.race?.find(r => r.id === item.race)?.official_name || item.race}, Kierowca: ${relatedData.driver?.find(d => d.id === item.driver)?.first_name + ' ' + relatedData.driver?.find(d => d.id === item.driver)?.last_name || item.driver}` :
                   item.first_name && item.last_name ? `${item.first_name} ${item.last_name}` : item.name || item.official_name || item.full_name}
                </option>
              ))}
            </select>
          </div>
        )}

        {selectedCategory && (
          <div className="form-container">
            <h2>{formData.id ? 'Edytuj' : 'Dodaj'} {selectedCategory}</h2>
            <form onSubmit={handleSubmit}>
              {fieldDefinitions.map((key) => (
                <div key={key} className="form-group">
                  <label>{key}: </label>
                  {relatedData[key] && Array.isArray(relatedData[key]) ? (
                    <select
                      name={key}
                      value={formData[key] || ''}
                      onChange={handleInputChange}
                    >
                      <option value="">-- Wybierz --</option>
                      {relatedData[key].map((relatedItem) => (
                        <option key={relatedItem.id} value={relatedItem.id}>
                          {relatedItem.first_name && relatedItem.last_name ? `${relatedItem.first_name} ${relatedItem.last_name}` : relatedItem.name || relatedItem.official_name || relatedItem.full_name}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type="text"
                      name={key}
                      value={formData[key] || ''}
                      onChange={handleInputChange}
                      readOnly={key === 'position' || key === 'points' ? Boolean(formData.id) : false}
                    />
                  )}
                </div>
              ))}
              <button type="submit">{formData.id ? 'Zaktualizuj' : 'Dodaj'}</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default ManagementPanel;