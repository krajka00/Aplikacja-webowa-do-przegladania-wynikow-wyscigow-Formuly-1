import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import axios from 'axios';
import Header from './Header';

jest.mock('axios');

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

beforeAll(() => {
  Object.defineProperty(window, 'localStorage', {
    value: (() => {
      let store = {};
      return {
        getItem: jest.fn((key) => store[key] || null),
        setItem: jest.fn((key, value) => {
          store[key] = value;
        }),
        clear: jest.fn(() => {
          store = {};
        }),
        removeItem: jest.fn((key) => {
          delete store[key];
        }),
      };
    })(),
    writable: true,
  });
});

describe('Header Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders banner and login link for unauthenticated users', async () => {
    localStorage.getItem.mockImplementation(() => null);

    await act(async () => {
      render(
        <MemoryRouter>
          <Header />
        </MemoryRouter>
      );
    });

    expect(screen.getByText('Formuła 1 - Wyniki Wyścigów')).toBeInTheDocument();
    expect(screen.getByText('Zaloguj')).toBeInTheDocument();
    expect(screen.queryByText('Wyloguj')).not.toBeInTheDocument();
    expect(screen.queryByText('Zarządzaj')).not.toBeInTheDocument();
  });

  test('renders admin button and logout for logged-in admin user', async () => {
    localStorage.getItem.mockImplementation((key) => {
      if (key === 'access_token') return 'mockAccessToken';
      if (key === 'is_admin') return 'true';
      return null;
    });

    await act(async () => {
      render(
        <MemoryRouter>
          <Header />
        </MemoryRouter>
      );
    });

    expect(screen.getByText('Zarządzaj')).toBeInTheDocument();
    expect(screen.getByText('Wyloguj')).toBeInTheDocument();
    expect(screen.queryByText('Zaloguj')).not.toBeInTheDocument();
  });

  test('handles logout functionality', async () => {
    localStorage.getItem.mockImplementation((key) => {
      if (key === 'access_token') return 'mockAccessToken';
      if (key === 'refresh_token') return 'mockRefreshToken';
      return null;
    });

    axios.post.mockResolvedValueOnce({});

    await act(async () => {
      render(
        <MemoryRouter>
          <Header />
        </MemoryRouter>
      );
    });

    const logoutButton = screen.getByText('Wyloguj');
    await act(async () => {
      fireEvent.click(logoutButton);
    });

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/api/logout/',
        { refresh: 'mockRefreshToken' },
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer mockAccessToken',
          },
        }
      );
    });

    expect(localStorage.clear).toHaveBeenCalled();
    expect(mockNavigate).toHaveBeenCalledWith('/');
    expect(screen.queryByText('Wyloguj')).not.toBeInTheDocument();
  });
});
