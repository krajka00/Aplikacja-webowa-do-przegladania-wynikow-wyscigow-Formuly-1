import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import DriverPage from './DriverPage';

jest.mock('axios');

describe('DriverPage Component', () => {
  const mockDriverData = {
    id: 1,
    first_name: 'Max',
    last_name: 'Verstappen',
    permanent_number: '33',
    abbreviation: 'VER',
    gender: 'Mężczyzna',
    date_of_birth: '1997-09-30',
    place_of_birth: 'Hasselt',
    country_of_birth: 1,
    date_of_death: null,
  };

  const mockCountryData = {
    id: 1,
    name: 'Holandia',
    demonym: 'Holender',
  };

  const mockStandingsData = [
    { id: 1, driver: 1, race: 1, position: 1, points: 25 },
    { id: 2, driver: 1, race: 2, position: 2, points: 18 },
  ];

  const mockRaceData = [
    { id: 1, official_name: 'Bahrain Grand Prix', date: '2023-03-05' },
    { id: 2, official_name: 'Saudi Arabian Grand Prix', date: '2023-03-19' },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state', async () => {
    axios.get.mockImplementation(() => new Promise(() => {}));

    render(
      <MemoryRouter initialEntries={['/driver/1']}>
        <Routes>
          <Route path="/driver/:pk" element={<DriverPage />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText(/Ładowanie danych kierowcy.../i)).toBeInTheDocument();
  });

  test('renders driver data and standings table', async () => {
    axios.get
      .mockResolvedValueOnce({ data: mockDriverData })
      .mockResolvedValueOnce({ data: mockCountryData })
      .mockResolvedValueOnce({ data: mockStandingsData })
      .mockResolvedValueOnce({ data: mockRaceData });

    render(
      <MemoryRouter initialEntries={['/driver/1']}>
        <Routes>
          <Route path="/driver/:pk" element={<DriverPage />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Szczegóły Kierowcy:/i)).toHaveTextContent('Max Verstappen');
    });

    expect(screen.getByText(/Numer stały:/i).parentElement).toHaveTextContent('33');
    expect(screen.getByText(/Skrót:/i).parentElement).toHaveTextContent('VER');
    expect(screen.getByText(/Płeć:/i).parentElement).toHaveTextContent('Mężczyzna');
    expect(screen.getByText(/Data urodzenia:/i).parentElement).toHaveTextContent('1997-09-30');
    expect(screen.getByText(/Miejsce urodzenia:/i).parentElement).toHaveTextContent('Hasselt');
    expect(screen.getByText(/Kraj urodzenia:/i).parentElement).toHaveTextContent('Holandia');
    expect(screen.getByText(/Narodowość:/i).parentElement).toHaveTextContent('Holender');

    await waitFor(() => {
      expect(screen.getByText(/Bahrain Grand Prix/i)).toBeInTheDocument();
      expect(screen.getByText(/Saudi Arabian Grand Prix/i)).toBeInTheDocument();
      expect(screen.getByText('25')).toBeInTheDocument();
      expect(screen.getByText('18')).toBeInTheDocument();
    });
  });

  test('renders error message on API failure', async () => {
    axios.get.mockRejectedValue(new Error('API Error'));

    render(
      <MemoryRouter initialEntries={['/driver/1']}>
        <Routes>
          <Route path="/driver/:pk" element={<DriverPage />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() =>
      expect(screen.getByText(/Nie udało się pobrać danych kierowcy, kraju lub wyników./i)).toBeInTheDocument()
    );
  });
});
