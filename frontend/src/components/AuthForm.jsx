import { useEffect, useState } from 'react'
import '../styles/index.css'

export default function AuthForm({ onSuccess, initialMode = 'login', onNavigate }) {
  const [mode, setMode] = useState(initialMode) // 'login' или 'register'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)
  const [emailHint, setEmailHint] = useState('')
  const [passHint, setPassHint] = useState('')

  useEffect(() => {
    setMode(initialMode)
    if (initialMode === 'register') {
      setEmailHint('Будет использоваться для входа')
      setPassHint('● Используйте буквы и цифры')
    } else {
      setEmailHint('')
      setPassHint('')
    }
    setError('')
  }, [initialMode])

  const validateEmail = (input) => {
    if (input.includes('@') && input.includes('.')) {
      setEmailHint('Email корректен')
      return true
    } else if (input.length > 0) {
      setEmailHint('Введите корректный email')
      return false
    } else {
      setEmailHint('Будет использоваться для входа')
      return false
    }
  }

  const validatePassword = (input) => {
    if (input.length >= 8) {
      setPassHint('● Надежный пароль')
      return true
    } else if (input.length > 0) {
      setPassHint('● Слишком короткий пароль')
      return false
    } else {
      setPassHint('● Используйте буквы и цифры')
      return false
    }
  }

  const handleEmailChange = (e) => {
    const value = e.target.value
    setEmail(value)
    validateEmail(value)
  }

  const handlePasswordChange = (e) => {
    const value = e.target.value
    setPassword(value)
    validatePassword(value)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const { apiClient } = await import('../api/client')

      if (mode === 'login') {
        await apiClient.login(email, password)
      } else {
        await apiClient.register(email, password, fullName || null)
        // После регистрации автоматически логиним
        await apiClient.login(email, password)
      }

      setShowSuccess(true)
      setTimeout(() => {
        onSuccess()
      }, 1500)

    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const switchMode = (newMode) => {
    setMode(newMode)
    setError('')
    if (newMode === 'register') {
      setEmailHint('Будет использоваться для входа')
      setPassHint('● Используйте буквы и цифры')
      onNavigate?.('/register')
    } else {
      setEmailHint('')
      setPassHint('')
      onNavigate?.('/login')
    }
  }

  return (
    <div className="auth-page">
      <div className="ambient-glow"></div>

      <header>
        <a href="/" className="logo-area" onClick={(e) => { e.preventDefault(); onNavigate?.('/') }}>
          <div className="logo-icon">
            <svg viewBox="0 0 24 24">
              <path d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 17l-2.5-7.25L12 11zm0 8l-5-2.5-5 2.5L12 22l10-3-5-2.5-5 2.5z"/>
            </svg>
          </div>
          <div className="logo-text">ItemGate</div>
        </a>
      </header>

      <main className="auth-main-content">
        <div className="auth-container" id="authBox">
          {/* Форма входа */}
          <div id="loginView" className={`view ${mode === 'login' ? 'active' : ''}`}>
            <div className="auth-header">
              <h2>Добро пожаловать</h2>
              <p>Войдите в свой аккаунт ItemGate</p>
            </div>

            <form id="loginForm" onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Электронная почта</label>
                <div className="input-wrapper">
                  <input
                    type="email"
                    className="form-input"
                    placeholder="example@mail.com"
                    value={email}
                    onChange={handleEmailChange}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Пароль</label>
                <div className="input-wrapper">
                  <input
                    type="password"
                    className="form-input"
                    placeholder="••••••••"
                    value={password}
                    onChange={handlePasswordChange}
                    required
                  />
                </div>
              </div>

              <div className="form-footer">
                <label style={{display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', color: 'var(--text-secondary)', cursor: 'pointer'}}>
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    style={{accentColor: 'var(--accent-cyan)'}}
                  />
                  Запомнить меня
                </label>
                <a href="#" className="recovery-link">Забыли пароль?</a>
              </div>

              <button type="submit" className="btn-submit" disabled={loading}>
                {loading ? '⏳ Вход...' : 'Войти в аккаунт'}
              </button>
            </form>

            <div className="toggle-mode">
              Нет аккаунта? <span className="toggle-link" onClick={() => switchMode('register')}>Зарегистрироваться</span>
            </div>
          </div>

          {/* Форма регистрации */}
          <div id="registerView" className={`view ${mode === 'register' ? 'active' : ''}`}>
            <div className="auth-header">
              <h2>Создать аккаунт</h2>
              <p>Начните оптимизацию карточек с ИИ</p>
            </div>

            <form id="registerForm" onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Имя</label>
                <div className="input-wrapper">
                  <input
                    type="text"
                    className="form-input"
                    placeholder="Иван Иванов"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Электронная почта</label>
                <div className="input-wrapper">
                  <input
                    type="email"
                    className="form-input"
                    placeholder="example@mail.com"
                    value={email}
                    onChange={handleEmailChange}
                    required
                  />
                </div>
                <div id="emailHint" className={`input-hint ${emailHint.includes('корректен') ? 'success' : emailHint.includes('корректный') ? 'error' : ''}`}>
                  {emailHint || 'Будет использоваться для входа'}
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Пароль</label>
                <div className="input-wrapper">
                  <input
                    type="password"
                    className="form-input"
                    placeholder="Минимум 8 символов"
                    value={password}
                    onChange={handlePasswordChange}
                    required
                  />
                </div>
                <div id="passHint" className={`input-hint ${passHint.includes('Надежный') ? 'success' : passHint.includes('короткий') ? 'error' : ''}`}>
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                  </svg>
                  {(passHint || '● Используйте буквы и цифры').replace('● ', '')}
                </div>
              </div>

              <button type="submit" className="btn-submit" disabled={loading}>
                {loading ? '⏳ Регистрация...' : 'Зарегистрироваться'}
              </button>
            </form>

            <div className="toggle-mode">
              Уже есть аккаунт? <span className="toggle-link" onClick={() => switchMode('login')}>Войти</span>
            </div>
          </div>

          {/* Оверлей успеха */}
          <div id="successOverlay" className={`success-overlay ${showSuccess ? 'show' : ''}`}>
            <div className="check-circle">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <h2 style={{marginBottom: '8px'}}>Успешно!</h2>
            <p style={{color: 'var(--text-secondary)', textAlign: 'center'}}>Переходим в личный кабинет...</p>
          </div>
        </div>
      </main>
    </div>
  )
}
