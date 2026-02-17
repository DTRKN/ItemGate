import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AuthForm from '../../components/AuthForm'
import { apiClient } from '../../api/client'

// Mock API client
vi.mock('../../api/client', () => ({
  apiClient: vi.fn(),
}))

describe('AuthForm Integration', () => {
  const mockApiClient = vi.mocked(apiClient)
  let user

  beforeEach(() => {
    user = userEvent.setup()
    mockApiClient.mockClear()
  })

  describe('Login Flow', () => {
    it('should successfully login user', async () => {
      const mockTokenResponse = {
        access_token: 'test-token-123',
        token_type: 'bearer'
      }

      const mockUserResponse = {
        id: 1,
        email: 'test@example.com',
        full_name: 'Test User',
        role: 'user',
        is_active: true
      }

      mockApiClient
        .mockResolvedValueOnce(mockTokenResponse) // login
        .mockResolvedValueOnce(mockUserResponse)  // get user profile

      const mockOnLogin = vi.fn()

      render(<AuthForm onLogin={mockOnLogin} />)

      // Переключаемся на вкладку логина
      const loginTab = screen.getByRole('tab', { name: /вход/i })
      await user.click(loginTab)

      // Заполняем форму
      const emailInput = screen.getByLabelText(/email/i)
      const passwordInput = screen.getByLabelText(/пароль/i)

      await user.type(emailInput, 'test@example.com')
      await user.type(passwordInput, 'password123')

      // Нажимаем кнопку входа
      const loginButton = screen.getByRole('button', { name: /войти/i })
      await user.click(loginButton)

      // Проверяем вызовы API
      await waitFor(() => {
        expect(mockApiClient).toHaveBeenCalledWith('/auth/login-json', {
          method: 'POST',
          body: JSON.stringify({
            email: 'test@example.com',
            password: 'password123'
          })
        })
      })

      // Проверяем вызов onLogin с данными пользователя
      await waitFor(() => {
        expect(mockOnLogin).toHaveBeenCalledWith(mockUserResponse)
      })
    })

    it('should show error on login failure', async () => {
      mockApiClient.mockRejectedValueOnce(new Error('Invalid credentials'))

      const mockOnLogin = vi.fn()

      render(<AuthForm onLogin={mockOnLogin} />)

      // Переключаемся на вкладку логина
      const loginTab = screen.getByRole('tab', { name: /вход/i })
      await user.click(loginTab)

      // Заполняем и отправляем форму
      const emailInput = screen.getByLabelText(/email/i)
      const passwordInput = screen.getByLabelText(/пароль/i)
      const loginButton = screen.getByRole('button', { name: /войти/i })

      await user.type(emailInput, 'wrong@example.com')
      await user.type(passwordInput, 'wrongpass')
      await user.click(loginButton)

      // Проверяем отображение ошибки
      await waitFor(() => {
        expect(screen.getByText(/ошибка входа/i)).toBeInTheDocument()
      })

      // onLogin не должен вызываться
      expect(mockOnLogin).not.toHaveBeenCalled()
    })
  })

  describe('Registration Flow', () => {
    it('should successfully register user', async () => {
      const mockRegisterResponse = {
        id: 1,
        email: 'newuser@example.com',
        full_name: 'New User',
        role: 'user',
        is_active: true
      }

      mockApiClient.mockResolvedValueOnce(mockRegisterResponse)

      const mockOnLogin = vi.fn()

      render(<AuthForm onLogin={mockOnLogin} />)

      // Остаемся на вкладке регистрации (по умолчанию)

      // Заполняем форму
      const emailInput = screen.getByLabelText(/email/i)
      const passwordInput = screen.getByLabelText(/пароль/i)
      const fullNameInput = screen.getByLabelText(/полное имя/i)

      await user.type(emailInput, 'newuser@example.com')
      await user.type(passwordInput, 'securepass123')
      await user.type(fullNameInput, 'New User')

      // Нажимаем кнопку регистрации
      const registerButton = screen.getByRole('button', { name: /зарегистрироваться/i })
      await user.click(registerButton)

      // Проверяем вызов API
      await waitFor(() => {
        expect(mockApiClient).toHaveBeenCalledWith('/auth/register', {
          method: 'POST',
          body: JSON.stringify({
            email: 'newuser@example.com',
            password: 'securepass123',
            full_name: 'New User'
          })
        })
      })

      // Проверяем вызов onLogin
      await waitFor(() => {
        expect(mockOnLogin).toHaveBeenCalledWith(mockRegisterResponse)
      })
    })

    it('should validate form fields', async () => {
      render(<AuthForm onLogin={vi.fn()} />)

      // Пытаемся отправить пустую форму
      const registerButton = screen.getByRole('button', { name: /зарегистрироваться/i })
      await user.click(registerButton)

      // Проверяем валидацию (предполагая, что она реализована)
      await waitFor(() => {
        expect(screen.getByText(/email обязателен/i)).toBeInTheDocument()
      })
    })
  })

  describe('Form Switching', () => {
    it('should switch between login and register tabs', async () => {
      render(<AuthForm onLogin={vi.fn()} />)

      // По умолчанию активна регистрация
      expect(screen.getByRole('tab', { name: /регистрация/i })).toHaveAttribute('aria-selected', 'true')

      // Переключаемся на логин
      const loginTab = screen.getByRole('tab', { name: /вход/i })
      await user.click(loginTab)

      expect(screen.getByRole('tab', { name: /вход/i })).toHaveAttribute('aria-selected', 'true')
      expect(screen.getByRole('tab', { name: /регистрация/i })).toHaveAttribute('aria-selected', 'false')

      // Проверяем, что поля логина отображаются
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/пароль/i)).toBeInTheDocument()
      expect(screen.queryByLabelText(/полное имя/i)).not.toBeInTheDocument()
    })
  })
})