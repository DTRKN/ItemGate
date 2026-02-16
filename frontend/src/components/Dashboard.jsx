import { useState, useEffect } from 'react'
import ItemCard from './ItemCard'
import ItemTabs from './ItemTabs'
import { apiClient } from '../api/client'

export default function Dashboard({ onLogout }) {
  const [activeTab, setActiveTab] = useState('main')
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [filterMarketplace, setFilterMarketplace] = useState('all')

  useEffect(() => {
    loadItems()
  }, [activeTab])

  const loadItems = async () => {
    setLoading(true)
    setError('')

    try {
      if (activeTab === 'main') {
        // Загружаем товары из каталога
        const catalogItems = await apiClient.getCatalogItems()
        setItems(catalogItems)
      } else if (activeTab === 'ai') {
        // Загружаем сгенерированные товары пользователя
        const userGenerations = await apiClient.getUserGenerations()
        setItems(userGenerations)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async (itemId) => {
    try {
      await apiClient.generateContent(itemId)
      // После генерации перезагружаем данные
      await loadItems()
      // Переключаемся на вкладку AI
      setActiveTab('ai')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleSave = async (generationId, data) => {
    try {
      await apiClient.updateGeneration(generationId, data)
      await loadItems()
    } catch (err) {
      setError(err.message)
    }
  }

  const filteredItems = items.filter(item => {
    const matchesSearch = !searchQuery ||
      (item.name && item.name.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (item.catalog_item?.name && item.catalog_item.name.toLowerCase().includes(searchQuery.toLowerCase()))

    const matchesMarketplace = filterMarketplace === 'all' ||
      (item.marketplace === filterMarketplace) ||
      (item.catalog_item?.marketplace === filterMarketplace)

    return matchesSearch && matchesMarketplace
  })

  return (
    <div style={{display: 'flex', minHeight: '100vh'}}>
      {/* Sidebar */}
      <aside className="sidebar">
        <a href="#" className="sidebar-logo">
          <div className="logo-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
              <path d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 17l-2.5-7.25L12 11zm0 8l-5-2.5-5 2.5L12 22l10-3-5-2.5-5 2.5z"/>
            </svg>
          </div>
          <span style={{fontWeight: 700, fontSize: '1.25rem'}}>SEOMate</span>
        </a>

        <ul className="nav-menu">
          <li>
            <a
              href="#"
              className={`nav-item ${activeTab === 'main' ? 'active' : ''}`}
              onClick={() => setActiveTab('main')}
            >
              Все товары
            </a>
          </li>
          <li>
            <a
              href="#"
              className={`nav-item ${activeTab === 'ai' ? 'active' : ''}`}
              onClick={() => setActiveTab('ai')}
            >
              Описание ИИ
            </a>
          </li>
          <li>
            <a href="#" className="nav-item">
              История генераций
            </a>
          </li>
          <li>
            <a href="#" className="nav-item">
              Загрузить товар
            </a>
          </li>
        </ul>

        <div style={{marginTop: 'auto', padding: '20px', background: 'rgba(0,194,255,0.05)', borderRadius: '12px'}}>
          <div style={{fontSize: '0.8rem', color: 'var(--accent-cyan)', fontWeight: 600, marginBottom: '4px'}}>
            PREMIUM PLAN
          </div>
          <div style={{fontSize: '0.75rem', color: 'var(--text-secondary)'}}>
            1,420 / 5,000 лимитов
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="dashboard-header">
          <h2 style={{fontSize: '1.4rem'}}>
            {activeTab === 'main' ? 'Дашборд' : 'Сгенерированные товары'}
          </h2>
          <div className="user-profile">
            <span className="user-email">m.ivanova@market.ru</span>
            <button className="logout-btn" onClick={onLogout}>Выйти</button>
          </div>
        </header>

        <div className="dashboard-container">
          {/* Search and Filter Row */}
          <div className="search-bar-row">
            <div className="search-input-wrapper">
              <input
                type="text"
                className="search-input"
                placeholder="Поиск товара по названию или артикулу..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <select
              className="filter-select"
              value={filterMarketplace}
              onChange={(e) => setFilterMarketplace(e.target.value)}
            >
              <option value="all">Все маркетплейсы</option>
              <option value="Wildberries">Wildberries</option>
              <option value="Ozon">Ozon</option>
            </select>
            <button className="btn-primary">Найти</button>
          </div>

          {/* Section Header */}
          <div className="section-header">
            <h3>
              {activeTab === 'main' ? 'Ваши товары' : 'Сгенерированные описания'}
            </h3>
            <div style={{display: 'flex', gap: '8px'}}>
              <button className="btn" style={{padding: '8px 16px', borderRadius: '8px', fontSize: '0.8rem', border: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.02)', color: 'white'}}>
                Сортировка: Дата
              </button>
            </div>
          </div>

          {/* Items Grid */}
          {loading ? (
            <div className="loading">Загрузка товаров...</div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : filteredItems.length === 0 ? (
            <div className="no-items">
              {activeTab === 'main' ? 'Нет товаров в каталоге' : 'Нет сгенерированных товаров'}
            </div>
          ) : (
            <div className="products-grid">
              {filteredItems.map(item => (
                <ItemCard
                  key={item.id}
                  item={item}
                  view={activeTab}
                  onGenerate={handleGenerate}
                  onSave={handleSave}
                  generating={false}
                />
              ))}
            </div>
          )}

          {/* History Table */}
          {activeTab === 'main' && (
            <>
              <div className="section-header">
                <h3>История генераций</h3>
                <a href="#" style={{color: 'var(--accent-cyan)', textDecoration: 'none', fontSize: '0.9rem'}}>
                  Смотреть все
                </a>
              </div>

              <div className="history-table-container">
                <table>
                  <thead>
                    <tr>
                      <th>Дата</th>
                      <th>Наименование товара</th>
                      <th>Результат</th>
                      <th>Действие</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>24.05.2024, 14:20</td>
                      <td>Смарт-часы Ultra X Pro Gen 2</td>
                      <td style={{color: 'var(--success-green)'}}>Оптимизировано (SEO 98%)</td>
                      <td>
                        <a href="#" className="btn-excel">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style={{marginRight: '4px'}}>
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14,2 14,8 20,8"/>
                          </svg>
                          Скачать Excel
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>23.05.2024, 11:05</td>
                      <td>Беспроводные наушники AirBass</td>
                      <td style={{color: 'var(--success-green)'}}>Оптимизировано (SEO 94%)</td>
                      <td>
                        <a href="#" className="btn-excel">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style={{marginRight: '4px'}}>
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14,2 14,8 20,8"/>
                          </svg>
                          Скачать Excel
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <td>22.05.2024, 18:45</td>
                      <td>Лампа настольная LED Smart</td>
                      <td style={{color: 'var(--text-secondary)'}}>Черновик описания</td>
                      <td>
                        <a href="#" className="btn-excel">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style={{marginRight: '4px'}}>
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14,2 14,8 20,8"/>
                          </svg>
                          Скачать Excel
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  )
}