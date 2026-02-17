import { describe, it, expect, vi, beforeEach } from 'vitest'
import { apiClient, setAuthToken, clearAuthToken } from '../api/client'

// Mock fetch
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('API Client', () => {
  beforeEach(() => {
    mockFetch.mockClear()
    clearAuthToken()
  })

  describe('setAuthToken / clearAuthToken', () => {
    it('should set and clear auth token', () => {
      const token = 'test-token-123'

      setAuthToken(token)
      expect(localStorage.setItem).toHaveBeenCalledWith('authToken', token)

      clearAuthToken()
      expect(localStorage.removeItem).toHaveBeenCalledWith('authToken')
    })
  })

  describe('apiClient', () => {
    it('should make GET request without auth', async () => {
      const mockResponse = { data: 'test' }
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      })

      const result = await apiClient('/test-endpoint')

      expect(mockFetch).toHaveBeenCalledWith('/test-endpoint', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      expect(result).toEqual(mockResponse)
    })

    it('should make POST request with auth token', async () => {
      const token = 'test-token'
      setAuthToken(token)

      const mockResponse = { success: true }
      const requestData = { email: 'test@example.com', password: 'pass123' }

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      })

      const result = await apiClient('/auth/login', {
        method: 'POST',
        body: JSON.stringify(requestData),
      })

      expect(mockFetch).toHaveBeenCalledWith('/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(requestData),
      })
      expect(result).toEqual(mockResponse)
    })

    it('should handle HTTP errors', async () => {
      const errorResponse = { detail: 'Not found' }
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: () => Promise.resolve(errorResponse),
      })

      await expect(apiClient('/not-found')).rejects.toThrow('HTTP 404')
    })

    it('should handle network errors', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'))

      await expect(apiClient('/test')).rejects.toThrow('Network error')
    })
  })
})