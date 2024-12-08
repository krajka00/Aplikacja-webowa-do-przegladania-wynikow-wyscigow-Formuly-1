import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import ConstructorPage from './ConstructorPage';

jest.mock('axios');

describe('ConstructorPage Component', () => {
  const mockConstructorData = {
    id: 1,
    name: 'Red Bull Racing',
    full_name: 'Oracle Red Bull Racing',
    country: 1,
  };

  const mockCountryData = {
    id: 1,
    name: 'Austria',
  };

  const mockStandingsData = [
    { id: 1, constructor: 1, race: 1, position: 1, points: 25 },
    { id: 2, constructor: 1, race: 2, position: 2, points: 18 },
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
      <MemoryRouter initialEntries={['/constructor/1']}>
        <Routes>
          <Route path="/constructor/:pk" element={<ConstructorPage />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText(/Ładowanie danych konstruktora.../i)).toBeInTheDocument();
  });

  test('renders constructor data and standings table', async () => {
    axios.get
      .mockResolvedValueOnce({ data: mockConstructorData })
      .mockResolvedValueOnce({ data: mockCountryData })
      .mockResolvedValueOnce({ data: mockStandingsData })
      .mockResolvedValueOnce({ data: mockRaceData });

    render(
      <MemoryRouter initialEntries={['/constructor/1']}>
        <Routes>
          <Route path="/constructor/:pk" element={<ConstructorPage />} />
        </Routes>
      </MemoryRouter>
    );

    // Debug: Sprawdź, co jest renderowane
    await waitFor(() => {
      console.log('DEBUG DOM:', screen.getByText(/Pełna nazwa:/i).parentElement.innerHTML);
    });

    // Sprawdź szczegóły konstruktora
    await waitFor(() => {
      const fullNameElement = screen.getByText(/Pełna nazwa:/i).parentElement;
      expect(fullNameElement).toHaveTextContent('Oracle Red Bull Racing');
    });

    await waitFor(() => {
      const countryElement = screen.getByText(/Kraj:/i).parentElement;
      expect(countryElement).toHaveTextContent('Austria');
    });

    // Sprawdź tabelę wyników
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
      <MemoryRouter initialEntries={['/constructor/1']}>
        <Routes>
          <Route path="/constructor/:pk" element={<ConstructorPage />} />
        </Routes>
      </MemoryRouter>
    );

    await waitFor(() =>
      expect(screen.getByText(/Nie udało się pobrać danych konstruktora lub jego wyników./i)).toBeInTheDocument()
    );
  });
});
