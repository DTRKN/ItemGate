import { useState, useEffect, useMemo } from 'react'
import AuthForm from './components/AuthForm'
import ItemCard from './components/ItemCard'
import { apiClient, authService } from './api/client'
import './styles/index.css'

export default function App() {
  const normalizePath = (path) => {
    const cleanPath = path.replace(/\/+$/, '') || '/'
    if (cleanPath === '/login' || cleanPath === '/register' || cleanPath === '/pricing') {
      return cleanPath
    }
    return '/'
  }

  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [authPath, setAuthPath] = useState(() => {
    const path = window.location.pathname
    return normalizePath(path)
  })
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Tab navigation
  const [tab, setTab] = useState('all')

  // Data states
  const [mainItems, setMainItems] = useState([])
  const [aiItems, setAiItems] = useState([])
  const [logs, setLogs] = useState([])

  // UI states
  const [credits, setCredits] = useState(0)
  const [isAdmin, setIsAdmin] = useState(false)
  const [searchWord, setSearchWord] = useState('')
  const [generatingIds, setGeneratingIds] = useState(new Set())

  // Pagination
  const [currentPageAll, setCurrentPageAll] = useState(1)
  const [currentPageAi, setCurrentPageAi] = useState(1)
  const [pageSize, setPageSize] = useState(25)

  // Upload states
  const [loadCount, setLoadCount] = useState(100)
  const [excelFile, setExcelFile] = useState(null)
  const [uploadResult, setUploadResult] = useState(null)
  const [uploadProgress, setUploadProgress] = useState('')
  const [isUploadingApi, setIsUploadingApi] = useState(false)

  // Проверка аутентификации при загрузке
  useEffect(() => {
    checkAuth()
  }, [])

  useEffect(() => {
    const handlePopState = () => {
      const path = window.location.pathname
      setAuthPath(normalizePath(path))
    }

    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [])

  const navigateTo = (path) => {
    if (window.location.pathname !== path) {
      window.history.pushState({}, '', path)
    }
    setAuthPath(normalizePath(path))
  }

  const renderPricingPage = () => (
    <div className="app pricing-page">
      <div className="ambient-glow"></div>

      <header className="pricing-header-bar">
        <div className="pricing-header-top">
          <div className="logo-area">
            <div className="logo-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
                <path d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 17l-2.5-7.25L12 11zm0 8l-5-2.5-5 2.5L12 22l10-3-5-2.5-5 2.5z"/>
              </svg>
            </div>
            <div className="logo-text">ItemGate</div>
          </div>
        </div>

        <div className="pricing-nav-row">
          <nav className="pricing-nav">
            <ul>
              <li><a href="#" onClick={(e) => { e.preventDefault(); navigateTo('/') }}>О сервисе</a></li>
              <li><a href="#" className="active" onClick={(e) => e.preventDefault()}>Тарифы</a></li>
              <li><a href="#reviews" onClick={(e) => { e.preventDefault(); navigateTo('/') }}>Контакты</a></li>
            </ul>
          </nav>

          <div className="pricing-auth-buttons">
            {isAuthenticated ? (
              <>
                <button className="btn btn-ghost" onClick={() => navigateTo('/')}>В кабинет</button>
                <button className="btn btn-primary" onClick={handleLogout}>Выйти</button>
              </>
            ) : (
              <>
                <button className="btn btn-ghost" onClick={() => navigateTo('/login')}>Войти</button>
                <button className="btn btn-primary" onClick={() => navigateTo('/register')}>Регистрация</button>
              </>
            )}
          </div>
        </div>
      </header>

      <main className="container pricing-main-container">
        <section className="pricing-section">
          <div className="pricing-section-header">
            <h1>Выберите свой план</h1>
            <p>Прозрачные условия без скрытых платежей. Масштабируйте ваш бизнес на маркетплейсах вместе с нами.</p>
          </div>

          <div className="pricing-grid">
            <div className="pricing-card">
              <div className="plan-name">Free</div>
              <div className="plan-price">
                <span className="price-amount">0</span>
                <span className="price-currency">₽</span>
                <span className="price-period">/ мес</span>
              </div>
              <ul className="plan-features">
                <li>✓ 5 карточек в месяц</li>
                <li>✓ Базовое SEO-описание</li>
                <li>✓ Анализ 1 конкурента</li>
                <li className="disabled">✕ Экспорт в Excel</li>
                <li className="disabled">✕ Приоритетная поддержка</li>
              </ul>
              <button className="btn btn-ghost" onClick={() => navigateTo('/register')}>Начать бесплатно</button>
            </div>

            <div className="pricing-card popular">
              <div className="badge-popular">Популярный</div>
              <div className="plan-name">Pro</div>
              <div className="plan-price">
                <span className="price-amount">2 900</span>
                <span className="price-currency">₽</span>
                <span className="price-period">/ мес</span>
              </div>
              <ul className="plan-features">
                <li>✓ 100 карточек в месяц</li>
                <li>✓ Продвинутая AI генерация</li>
                <li>✓ Безлимитный анализ ниши</li>
                <li>✓ Экспорт в Excel/CSV</li>
                <li className="disabled">✕ Персональный менеджер</li>
              </ul>
              <button className="btn btn-primary" onClick={() => navigateTo('/register')}>Выбрать Pro</button>
            </div>

            <div className="pricing-card">
              <div className="plan-name">Premium+</div>
              <div className="plan-price">
                <span className="price-amount">7 500</span>
                <span className="price-currency">₽</span>
                <span className="price-period">/ мес</span>
              </div>
              <ul className="plan-features">
                <li>✓ Безлимитные карточки</li>
                <li>✓ Кастомные промпты ИИ</li>
                <li>✓ API интеграция</li>
                <li>✓ Мультиаккаунт (до 5 чел)</li>
                <li>✓ Поддержка 24/7</li>
              </ul>
              <button className="btn btn-ghost" onClick={() => navigateTo('/register')}>Связаться с нами</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  )

  const checkAuth = async () => {
    if (!authService.isAuthenticated()) {
      setIsAuthenticated(false)
      setLoading(false)
      return
    }

    try {
      const user = await apiClient.getMe()
      setCurrentUser(user)
      setCredits(user.credits || 0)
      const userEmail = (user.email || '').toLowerCase()
      const userRole = (user.role || '').toLowerCase()
      setIsAdmin(userRole === 'admin' || userEmail === 'test@test.com')
      setIsAuthenticated(true)
      await fetchMainItems()
    } catch (err) {
      setIsAuthenticated(false)
      authService.removeToken()
    } finally {
      setLoading(false)
    }
  }

  const fetchMainItems = async () => {
    try {
      const data = await apiClient.getItems()
      setMainItems(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Error fetching main items:', err)
    }
  }

  const fetchAiItems = async () => {
    try {
      const data = await apiClient.getItemsSellers()
      setAiItems(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Error fetching AI items:', err)
    }
  }

  const handleAuthSuccess = async () => {
    await checkAuth()
    navigateTo('/')
  }

  const handleLogout = () => {
    apiClient.logout()
    setIsAuthenticated(false)
    navigateTo('/')
    setCurrentUser(null)
    setCredits(0)
    setIsAdmin(false)
    setTab('all')
  }

  const handleGenerate = async (catalog_item_id) => {
    // сразу переносим карточку в вкладку AI, показываем статус создания
    setGeneratingIds(prev => new Set(prev).add(catalog_item_id))

    try {
      const result = await apiClient.generateDescription(catalog_item_id)
      if (result && result.error) {
        throw new Error(result.error)
      }
      // после генерации обновим оба списка
      await fetchMainItems()
      await fetchAiItems()
      setTab('ai')
      setCurrentPageAi(1)
    } catch (err) {
      console.error('AI generation error:', err)
      alert('Ошибка при генерации: ' + (err.message || 'Неизвестная ошибка'))
    } finally {
      setGeneratingIds(prev => {
        const copy = new Set(prev)
        copy.delete(catalog_item_id)
        return copy
      })
    }
  }

  const handleSearch = async (e) => {
    e?.preventDefault()
    if (!searchWord.trim()) {
      if (tab === 'ai') {
        await fetchAiItems()
      } else {
        await fetchMainItems()
      }
      return
    }

    setLoading(true)
    setError(null)
    try {
      if (tab === 'ai') {
        const data = await apiClient.searchGeneratedItems(searchWord)
        setAiItems(Array.isArray(data) ? data : [])
        setCurrentPageAi(1)
      } else {
        const data = await apiClient.searchItems(searchWord)
        setMainItems(Array.isArray(data) ? data : [])
        setCurrentPageAll(1)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleLoadItems = async (e) => {
    e?.preventDefault()
    setIsUploadingApi(true)
    setUploadProgress('Начинаю загрузку...')
    setError(null)

    try {
      const token = authService.getToken()

      // Используем fetch вместо EventSource для отправки токена
      const response = await fetch(`http://localhost:8000/sima-land/loading_words_db/${loadCount}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        throw new Error('Ошибка загрузки товаров')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const text = decoder.decode(value)
        const lines = text.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const message = line.slice(6)
            setUploadProgress(message)
          } else if (line.trim()) {
            // В некоторых ответах сервер шлёт просто текст без префикса
            setUploadProgress(line.trim())
          }
        }
      }

      await fetchMainItems()

    } catch (err) {
      setError(err.message)
      setUploadProgress('Ошибка: ' + (err.message || 'Неизвестная ошибка'))
    } finally {
      setIsUploadingApi(false)
    }
  }

  const handleSaveItem = async (generation_id, payload) => {
    setLoading(true)
    try {
      await apiClient.updateItem(generation_id, payload)
      await fetchAiItems()
      setTab('ai')
    } catch (err) {
      alert('Ошибка сохранения: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFetchLogs = async () => {
    setLoading(true)
    try {
      const data = await apiClient.getLogs()
      setLogs(Array.isArray(data) ? data : [])
    } catch (err) {
      setLogs([])
    } finally {
      setLoading(false)
    }
  }

  // === EXCEL HANDLERS ===
  const handleExcelUpload = async (e) => {
    e?.preventDefault()
    if (!excelFile) {
      alert('Выберите файл Excel')
      return
    }

    setLoading(true)
    setUploadResult(null)

    try {
      const result = await apiClient.uploadExcel(excelFile)
      setUploadResult(result)
      setExcelFile(null)
      await fetchMainItems()
    } catch (err) {
      alert('Ошибка загрузки: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadBackup = async () => {
    setLoading(true)
    try {
      await apiClient.downloadBackup()
    } catch (err) {
      alert('Ошибка скачивания бэкапа: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleExportItems = async () => {
    setLoading(true)
    try {
      await apiClient.exportItems()
    } catch (err) {
      alert('Ошибка экспорта: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  // add generating items to AI list temporarily
  const aiItemsWithGenerating = useMemo(() => {
    return aiItems.concat(
      mainItems.filter(i => generatingIds.has(i.id_item) || generatingIds.has(i.id))
    )
  }, [aiItems, mainItems, generatingIds])

  // pagination with separate page per tab
  const paginateAll = () => {
    const start = (currentPageAll - 1) * pageSize
    return mainItems.slice(start, start + pageSize)
  }

  const paginateAi = () => {
    const start = (currentPageAi - 1) * pageSize
    return aiItemsWithGenerating.slice(start, start + pageSize)
  }

  const totalAll = mainItems.length
  const totalAi = aiItemsWithGenerating.length
  const pagesAll = Math.max(1, Math.ceil(totalAll / pageSize))
  const pagesAi = Math.max(1, Math.ceil(totalAi / pageSize))

  if (loading && !isUploadingApi) {
    return (
      <div className="app">
        <div className="loading">Загрузка...</div>
      </div>
    )
  }

  if (authPath === '/pricing') {
    return renderPricingPage()
  }

  // Если не авторизован - показываем форму входа
  if (!isAuthenticated) {
    if (authPath === '/login' || authPath === '/register') {
      return (
        <AuthForm
          key={authPath}
          onSuccess={handleAuthSuccess}
          initialMode={authPath === '/register' ? 'register' : 'login'}
          onNavigate={navigateTo}
        />
      )
    }
    return (
      <div className="app landing-page">
        <div className="ambient-glow"></div>

        <header className="landing-header">
          <div className="landing-header-top">
            <div className="logo-area">
              <div className="logo-icon">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
                  <path d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 17l-2.5-7.25L12 11zm0 8l-5-2.5-5 2.5L12 22l10-3-5-2.5-5 2.5z"/>
                </svg>
              </div>
              <div className="logo-text">ItemGate</div>
            </div>
            <div className="landing-tagline">Автоматизация SEO-карточек для маркетплейсов</div>
          </div>

          <div className="landing-nav-row">
            <nav className="landing-nav">
              <ul>
                <li><a href="#features">О сервисе</a></li>
                <li><a href="#" onClick={(e) => { e.preventDefault(); navigateTo('/pricing') }}>Тарифы</a></li>
                <li><a href="#integrations">Интеграции</a></li>
                <li><a href="#reviews">Отзывы</a></li>
              </ul>
            </nav>
            <div className="landing-auth-buttons">
              <button className="btn btn-ghost" onClick={() => navigateTo('/login')}>Войти</button>
              <button className="btn btn-primary" onClick={() => navigateTo('/register')}>Регистрация</button>
            </div>
          </div>
        </header>

        <main className="container landing-main">
          <section className="landing-hero" id="features">
            <div className="landing-hero-content">
              <div className="landing-hero-label">Доступно в Premium+</div>
              <h1>Генерация карточек с помощью AI</h1>
              <p className="landing-hero-desc">
                Увеличьте продажи на маркетплейсах благодаря умной SEO-оптимизации и автоматическому созданию продающего контента.
              </p>

              <div className="landing-feature-list">
                <div className="landing-feature-item">
                  <div className="check-icon">✓</div>
                  <div>
                    <h4>Умный подбор ключевых слов</h4>
                    <p>Анализ конкурентов и трендов в реальном времени</p>
                  </div>
                </div>
                <div className="landing-feature-item">
                  <div className="check-icon">✓</div>
                  <div>
                    <h4>Генерация описаний</h4>
                    <p>Уникальные тексты, оптимизированные для поиска</p>
                  </div>
                </div>
                <div className="landing-feature-item">
                  <div className="check-icon">✓</div>
                  <div>
                    <h4>Интеграция с Excel</h4>
                    <p>Массовая загрузка и выгрузка данных без ограничений</p>
                  </div>
                </div>
              </div>

              <div className="landing-cta-area">
                <button className="btn btn-primary cta-btn" onClick={() => navigateTo('/register')}>
                  Попробовать бесплатно
                </button>
              </div>
            </div>

            <div className="landing-hero-visual">
              <div className="card-stack">
                <div className="ui-card back"></div>
                <div className="ui-card mid"></div>
                <div className="ui-card front">
                  <div className="card-header">
                    <div className="card-icon-lg">
                      <svg width="32" height="32" viewBox="0 0 24 24" fill="#00C2FF">
                        <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8h16v10zm-2-6H6v2h12v-2z"/>
                      </svg>
                    </div>
                    <div className="card-pill">AI Processing</div>
                    <div className="card-title">Оптимизация...</div>
                    <p style={{color: 'var(--text-secondary)', fontSize: '0.9rem'}}>Генерация SEO-тегов для категории "Электроника"</p>
                  </div>
                  
                  <div style={{display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px'}}>
                    <div style={{height: '8px', width: '100%', background: 'rgba(255,255,255,0.05)', borderRadius: '4px'}}></div>
                    <div style={{height: '8px', width: '80%', background: 'rgba(255,255,255,0.05)', borderRadius: '4px'}}></div>
                    <div style={{height: '8px', width: '90%', background: 'rgba(255,255,255,0.05)', borderRadius: '4px'}}></div>
                  </div>

                  <div className="loading-bar">
                    <div className="loading-progress"></div>
                  </div>
                </div>
              </div>

              <div className="float-badge fb-1">
                <span style={{color: '#2ECC71'}}>●</span> Excel Export
              </div>
              <div className="float-badge fb-2">
                <span style={{color: '#00C2FF'}}>●</span> SEO 100%
              </div>
            </div>
          </section>

          <section className="landing-bottom" id="integrations">
            <h3 style={{textAlign: 'center', color: 'var(--text-secondary)', fontWeight: '500'}}>Интеграция с платформами</h3>
            <div className="logos-row">
              <div className="logo-item">
                <span style={{color: '#217346', background: 'white', padding: '2px 8px', borderRadius: '4px'}}>X</span> Microsoft Excel
              </div>
              <div className="logo-item">
                <span style={{color: '#f53b7c', fontSize: '1.2rem'}}>✿</span> Sima-Land
              </div>
              <div className="logo-item">
                WB Partners
              </div>
              <div className="logo-item">
                Ozon Seller
              </div>
            </div>

            <div className="testimonials" id="reviews">
              <div className="testimonial-card">
                <p style={{color: 'var(--text-secondary)', lineHeight: '1.6'}}>"Сервис сэкономил нам часы работы. Карточки выходят в топ уже через неделю после оптимизации."</p>
                <div className="user-info">
                  <div className="avatar" style={{background: 'linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%)'}}></div>
                  <div>
                    <div style={{fontWeight: '600'}}>Алексей Петров</div>
                    <div style={{fontSize: '0.8rem', color: 'var(--text-secondary)'}}>Seller on Wildberries</div>
                  </div>
                </div>
              </div>
              <div className="testimonial-card">
                <p style={{color: 'var(--text-secondary)', lineHeight: '1.6'}}>"Отличная автоматизация. ИИ пишет описания лучше, чем наши копирайтеры."</p>
                <div className="user-info">
                  <div className="avatar" style={{background: 'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)'}}></div>
                  <div>
                    <div style={{fontWeight: '600'}}>Мария Иванова</div>
                    <div style={{fontSize: '0.8rem', color: 'var(--text-secondary)'}}>Ozon Manager</div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    )
  }

  return (
    <div className="app workspace-page">
      <div className="ambient-glow"></div>

      <header className="header workspace-headerbar">
        <div className="container header-content workspace-header-content">
          <a href="/" className="logo-area">
            <div className="logo-icon">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="white">
                <path d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 17l-2.5-7.25L12 11zm0 8l-5-2.5-5 2.5L12 22l10-3-5-2.5-5 2.5z"/>
              </svg>
            </div>
            <div className="logo-text">ItemGate</div>
          </a>

          <nav className="nav-menu">
            <button className={`nav-link ${tab==='all'?'active':''}`} onClick={() => setTab('all')}>
              Все товары
            </button>
            <button className={`nav-link ${tab==='ai'?'active':''}`} onClick={() => { setTab('ai'); fetchAiItems(); }}>
              Описание ИИ
            </button>
            {isAdmin && (
              <>
                <button className={`nav-link ${tab==='logs'?'active':''}`} onClick={() => { setTab('logs'); handleFetchLogs(); }}>
                  Log
                </button>
                <button className={`nav-link ${tab==='upload'?'active':''}`} onClick={() => setTab('upload')}>
                  Download item
                </button>
              </>
            )}
          </nav>

          <div className="header-actions">
            <div className="credits-display">
              <span className="credits-label">Генераций доступно:</span>
              <span className="credits-value">{credits}</span>
            </div>

            <div className="user-menu">
              <div className="user-avatar">
                <div className="avatar-circle"></div>
              </div>
              <div className="user-details">
                <span className="user-email">{currentUser?.email}</span>
                {isAdmin && <span className="admin-indicator">ADMIN</span>}
              </div>
              <button onClick={handleLogout} className="btn-secondary logout-btn">
                Выйти
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          <div className="content-wrapper">
            {tab === 'upload' && isAdmin && (
              <div className="upload-panel">
                <div className="panel-header">
                  <h2>Загрузка товаров из Sima-Land</h2>
                </div>
                <div className="panel-content">
                  <form onSubmit={handleLoadItems} className="load-form">
                    <div className="form-group">
                      <label>Количество товаров:</label>
                      <input
                        type="number"
                        min="1"
                        max="10000"
                        value={loadCount}
                        onChange={(e) => setLoadCount(parseInt(e.target.value))}
                        className="form-input"
                      />
                    </div>
                    <button type="submit" className="btn-primary" disabled={isUploadingApi}>{isUploadingApi ? 'Загрузка...' : 'Загрузить из API'}</button>
                  </form>

                  <div className="section-divider">
                    <h3>Загрузка товаров из Excel</h3>
                  </div>
                  <div className="excel-upload">
                    <form onSubmit={handleExcelUpload} className="load-form">
                      <div className="form-group">
                        <label>Выберите файл Excel:</label>
                        <input
                          type="file"
                          accept=".xlsx,.xls"
                          onChange={(e) => setExcelFile(e.target.files[0])}
                          className="form-input"
                        />
                      </div>
                      <button type="submit" disabled={!excelFile} className="btn-primary">
                        Загрузить Excel
                      </button>
                    </form>
                    <p className="form-hint">
                      Обязательные колонки: id_item, name, price, photoUrl, slug
                      (опционально: description/raw_description, stuff, category_id, balance)
                    </p>
                  </div>

                  {uploadResult && (
                    <div className="upload-result">
                      <h4>Результаты загрузки:</h4>
                      <div className="result-stats">
                        <p>✅ Добавлено: {uploadResult.added}</p>
                        <p>⊘ Пропущено: {uploadResult.skipped}</p>
                      </div>
                      {uploadResult.errors.length > 0 && (
                        <div className="errors-section">
                          <h5>Ошибки:</h5>
                          <ul className="error-list">
                            {uploadResult.errors.map((err, idx) => (
                              <li key={idx}>{err}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  {uploadProgress && (
                    <div className="upload-progress">
                      <div className="progress-text">{uploadProgress}</div>
                    </div>
                  )}

                  <div className="export-section">
                    <h3>Экспорт и Бэкапы</h3>
                    <div className="action-buttons">
                      <button onClick={handleExportItems} className="btn-secondary">
                        📥 Экспорт товаров в Excel
                      </button>
                      <button onClick={handleDownloadBackup} className="btn-secondary">
                        💾 Скачать полный бэкап БД
                      </button>
                      <button onClick={fetchMainItems} className="btn-primary">
                        🔄 Обновить список
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {tab === 'logs' && isAdmin && (
              <div className="logs-panel">
                <div className="panel-header">
                  <h2>Системные логи</h2>
                </div>
                <div className="panel-content">
                  {loading && <div className="loading">Загрузка логов...</div>}
                  {!loading && logs.length === 0 && <div className="no-items">Логи не найдены</div>}
                  {!loading && logs.length > 0 && (
                    <div className="logs-table-container">
                      <table className="logs-table">
                        <thead>
                          <tr>
                            <th>Время</th>
                            <th>Действие</th>
                            <th>ID Товара</th>
                            <th>Сообщение</th>
                            <th>Статус</th>
                          </tr>
                        </thead>
                        <tbody>
                          {logs.map((log, idx) => (
                            <tr key={idx}>
                              <td>{new Date(log.timestamp).toLocaleString('ru-RU')}</td>
                              <td>{log.action}</td>
                              <td>{log.item_id || '-'}</td>
                              <td>{log.message}</td>
                              <td>
                                <span className={`status-badge status-${log.status}`}>
                                  {log.status}
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </div>
            )}

            {(tab === 'all' || tab === 'ai') && (
              <div className="items-section">
                <div className="section-header">
                  <h2>
                    {tab === 'all' ? 'Все товары' : 'Генерация описаний ИИ'}
                  </h2>
                  <form onSubmit={handleSearch} className="search-form workspace-search-form">
                    <input
                      type="text"
                      placeholder="Поиск товара..."
                      value={searchWord}
                      onChange={(e) => setSearchWord(e.target.value)}
                      className="search-input"
                    />
                    <button type="submit" className="btn-primary search-btn workspace-search-btn">Искать</button>
                  </form>
                </div>

                <div className="section-content">
                  {error && <div className="error-message">{error}</div>}
                  {loading && <div className="loading">Загрузка...</div>}

                  <div className="items-grid">
                    {tab === 'all' && paginateAll().map((item) => (
                      <ItemCard
                        key={item.id_item || item.id}
                        item={item}
                        view="main"
                        onGenerate={handleGenerate}
                      />
                    ))}

                    {tab === 'ai' && paginateAi().map((item) => (
                      <ItemCard
                        key={item.id_item || item.id}
                        item={item}
                        view="ai"
                        generating={generatingIds.has(item.id_item || item.id)}
                        onSave={handleSaveItem}
                        onExport={handleExportItems}
                      />
                    ))}

                    {((tab === 'all' && totalAll === 0) || (tab === 'ai' && totalAi === 0)) && !loading && (
                      <div className="no-items">Товары не найдены</div>
                    )}
                  </div>

                  {tab === 'all' && (
                    <div className="pagination">
                      <button
                        onClick={() => setCurrentPageAll(p => Math.max(1, p-1))}
                        disabled={currentPageAll===1}
                        className="btn-secondary"
                      >
                        Предыдущая
                      </button>
                      <span className="page-info">
                        Страница {currentPageAll} из {pagesAll}
                      </span>
                      <button
                        onClick={() => setCurrentPageAll(p => Math.min(pagesAll, p+1))}
                        disabled={currentPageAll===pagesAll}
                        className="btn-secondary"
                      >
                        Следующая
                      </button>
                      <select
                        value={pageSize}
                        onChange={(e) => { setPageSize(parseInt(e.target.value)); setCurrentPageAll(1); }}
                        className="page-size-select"
                      >
                        <option value={10}>10</option>
                        <option value={25}>25</option>
                        <option value={50}>50</option>
                        <option value={100}>100</option>
                      </select>
                    </div>
                  )}

                  {tab === 'ai' && (
                    <div className="pagination">
                      <button
                        onClick={() => setCurrentPageAi(p => Math.max(1, p-1))}
                        disabled={currentPageAi===1}
                        className="btn-secondary"
                      >
                        Предыдущая
                      </button>
                      <span className="page-info">
                        Страница {currentPageAi} из {pagesAi}
                      </span>
                      <button
                        onClick={() => setCurrentPageAi(p => Math.min(pagesAi, p+1))}
                        disabled={currentPageAi===pagesAi}
                        className="btn-secondary"
                      >
                        Следующая
                      </button>
                      <select
                        value={pageSize}
                        onChange={(e) => { setPageSize(parseInt(e.target.value)); setCurrentPageAi(1); }}
                        className="page-size-select"
                      >
                        <option value={10}>10</option>
                        <option value={25}>25</option>
                        <option value={50}>50</option>
                        <option value={100}>100</option>
                      </select>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
