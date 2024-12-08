import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import HomePage from './HomePage';
import axios from 'axios';

jest.mock('axios');

describe('HomePage Component', () => {
  const mockRaces = [
    {
      id: 1,
      official_name: 'Bahrain Grand Prix',
      date: '2023-03-05',
      round: 1,
    },
    {
      id: 2,
      official_name: 'Saudi Arabian Grand Prix',
      date: '2023-03-19',
      round: 2,
    },
  ];

  const mockDriverStandings = [
    {
      position: 1,
      driver: 'Max Verstappen',
      driver_id: 1,
      points: 25,
    },
    {
      position: 2,
      driver: 'Lewis Hamilton',
      driver_id: 2,
      points: 18,
    },
  ];

  const mockConstructorStandings = [
    {
      position: 1,
      constructor: 'Red Bull Racing',
      constructor_id: 1,
      points: 43,
    },
    {
      position: 2,
      constructor: 'Mercedes',
      constructor_id: 2,
      points: 27,
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders race list, driver standings, and constructor standings', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('/api/races/all/2023')) {
        return Promise.resolve({ data: mockRaces });
      }
      if (url.includes('/api/standings/current/')) {
        return Promise.resolve({
          data: {
            driver_standings: mockDriverStandings,
            constructor_standings: mockConstructorStandings,
          },
        });
      }
      return Promise.reject(new Error('Unexpected API call'));
    });

    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>
    );

    // Verify race list
    await waitFor(() => {
      expect(screen.getByText('Bahrain Grand Prix')).toBeInTheDocument();
      expect(screen.getByText('Saudi Arabian Grand Prix')).toBeInTheDocument();
    });

    // Verify driver standings
    await waitFor(() => {
      expect(screen.getByText('Max Verstappen')).toBeInTheDocument();
      expect(screen.getByText('Lewis Hamilton')).toBeInTheDocument();
    });

    // Verify constructor standings
    await waitFor(() => {
      expect(screen.getByText('Red Bull Racing')).toBeInTheDocument();
      expect(screen.getByText('Mercedes')).toBeInTheDocument();
    });

    // Verify API calls
    expect(axios.get).toHaveBeenCalledWith('http://127.0.0.1:8000/api/races/all/2023');
    expect(axios.get).toHaveBeenCalledWith('http://127.0.0.1:8000/api/standings/current/');
  });

  test('handles API errors gracefully', async () => {
    axios.get.mockRejectedValue(new Error('API error'));

    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.queryByText('Bahrain Grand Prix')).not.toBeInTheDocument();
      expect(screen.queryByText('Red Bull Racing')).not.toBeInTheDocument();
      expect(screen.queryByText('Max Verstappen')).not.toBeInTheDocument();
    });
  });
});
