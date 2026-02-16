import { useState } from 'react'
import { apiClient } from '../api/client'

export default function CreateItem({ onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    marketplace: 'Wildberries',
    category: 'Электроника',
    characteristics: '',
    keywords: []
  })
  const [newKeyword, setNewKeyword] = useState('')
  const [aiSettings, setAiSettings] = useState({
    competitorAnalysis: true,
    lsiCopywriting: true,
    tone: 'selling',
    length: 'optimal'
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleAddKeyword = (e) => {
    if (e.key === 'Enter' && newKeyword.trim()) {
      const keyword = newKeyword.trim()
      if (!formData.keywords.includes(keyword)) {
        setFormData(prev => ({
          ...prev,
          keywords: [...prev.keywords, keyword]
        }))
      }
      setNewKeyword('')
      e.preventDefault()
    }
  }

  const handleRemoveKeyword = (index) => {
    setFormData(prev => ({
      ...prev,
      keywords: prev.keywords.filter((_, i) => i !== index)
    }))
  }

  const handleAiSettingChange = (setting, value) => {
    setAiSettings(prev => ({ ...prev, [setting]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // Создаем товар через API (если есть) или показываем сообщение
      // Пока что просто симулируем создание
      alert('Функция создания товара будет реализована после добавления соответствующего API в бэкенд. См. файл MISSING_BACKEND.md')

      if (onSuccess) onSuccess()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="ambient-glow"></div>

      <header style={{
        padding: 'var(--space-m) 0',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        background: 'rgba(3, 11, 24, 0.8)',
        backdropFilter: 'blur(10px)',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div style={{maxWidth: '1200px', margin: '0 auto', padding: '0 var(--space-m)'}}>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
            <a href="/" className="logo-area">
              <div className="logo-icon">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="white">
                  <path d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 17l-2.5-7.25L12 11zm0 8l-5-2.5-5 2.5L12 22l10-3-5-2.5-5 2.5z"/>
                </svg>
              </div>
              <div className="logo-text">SEOMate</div>
            </a>
            <div style={{display: 'flex', gap: '20px', alignItems: 'center'}}>
              <span style={{color: 'var(--text-secondary)', fontSize: '0.9rem'}}>
                Доступно генераций: <strong style={{color: 'white'}}>148</strong>
              </span>
              <div style={{width: '32px', height: '32px', borderRadius: '50%', background: 'var(--grad-primary)'}}></div>
            </div>
          </div>
        </div>
      </header>

      <main className="page-wrapper">
        <div className="container">
          <div className="form-grid">
            <div className="card-main">
              <h2 className="section-title">Новая карточка товара</h2>
              <p className="section-desc">Заполните базовую информацию, и наш ИИ подготовит оптимизированный контент.</p>

              {error && <div className="error-message">{error}</div>}

              <form onSubmit={handleSubmit}>
                <div className="input-group">
                  <label className="label">Название товара</label>
                  <input
                    type="text"
                    className="input-field"
                    placeholder="Например: Смарт-часы Ultra X8 Pro"
                    value={formData.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                    required
                  />
                </div>

                <div className="select-grid">
                  <div className="input-group">
                    <label className="label">Маркетплейс</label>
                    <select
                      className="input-field"
                      value={formData.marketplace}
                      onChange={(e) => handleInputChange('marketplace', e.target.value)}
                    >
                      <option>Wildberries</option>
                      <option>Ozon</option>
                      <option>Yandex Market</option>
                    </select>
                  </div>
                  <div className="input-group">
                    <label className="label">Категория</label>
                    <select
                      className="input-field"
                      value={formData.category}
                      onChange={(e) => handleInputChange('category', e.target.value)}
                    >
                      <option>Электроника</option>
                      <option>Одежда и аксессуары</option>
                      <option>Дом и сад</option>
                      <option>Красота и здоровье</option>
                    </select>
                  </div>
                </div>

                <div className="input-group">
                  <label className="label">Основные характеристики</label>
                  <textarea
                    className="input-field"
                    placeholder="Опишите ключевые особенности товара, которые важно упомянуть в тексте..."
                    value={formData.characteristics}
                    onChange={(e) => handleInputChange('characteristics', e.target.value)}
                    rows={4}
                  />
                </div>

                <div className="input-group">
                  <label className="label">Ключевые слова (SEO)</label>
                  <div className="keyword-tags">
                    {formData.keywords.map((keyword, index) => (
                      <div key={index} className="keyword-tag">
                        {keyword}
                        <span className="close" onClick={() => handleRemoveKeyword(index)}>×</span>
                      </div>
                    ))}
                  </div>
                  <input
                    type="text"
                    className="input-field"
                    placeholder="Добавьте свои ключи или оставьте пустым для автоподбора"
                    value={newKeyword}
                    onChange={(e) => setNewKeyword(e.target.value)}
                    onKeyPress={handleAddKeyword}
                  />
                </div>
              </form>
            </div>

            <div className="sidebar-settings">
              <div className="settings-card">
                <h3 className="settings-title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 15V3m0 12l-4-4m4 4l4-4M2 17l.621 2.485A2 2 0 004.561 21h14.878a2 2 0 001.94-1.515L22 17"/>
                  </svg>
                  Параметры ИИ
                </h3>

                <div className="toggle-row">
                  <span className="toggle-label">Анализ конкурентов <span className="premium-badge">PRO</span></span>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={aiSettings.competitorAnalysis}
                      onChange={(e) => handleAiSettingChange('competitorAnalysis', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="toggle-row">
                  <span className="toggle-label">LSI-копирайтинг</span>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={aiSettings.lsiCopywriting}
                      onChange={(e) => handleAiSettingChange('lsiCopywriting', e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="toggle-row">
                  <span className="toggle-label">Тон голоса: Продающий</span>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={aiSettings.tone === 'selling'}
                      onChange={(e) => handleAiSettingChange('tone', e.target.checked ? 'selling' : 'neutral')}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="input-group" style={{marginTop: '16px', marginBottom: '0'}}>
                  <label className="label">Длина текста</label>
                  <select
                    className="input-field"
                    style={{fontSize: '0.9rem'}}
                    value={aiSettings.length}
                    onChange={(e) => handleAiSettingChange('length', e.target.value)}
                  >
                    <option value="optimal">Оптимальная (1500-2000 зн.)</option>
                    <option value="short">Краткая (до 1000 зн.)</option>
                    <option value="long">Максимальная (3000+ зн.)</option>
                  </select>
                </div>
              </div>

              <button className="btn-generate" onClick={handleSubmit} disabled={loading}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71L12 2z"/>
                </svg>
                {loading ? 'Создание...' : 'Сгенерировать'}
              </button>

              <p style={{textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-secondary)'}}>
                Будет списано 1 кредитное очко
              </p>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}