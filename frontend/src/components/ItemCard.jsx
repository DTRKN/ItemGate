import { useState } from 'react'

export default function ItemCard({ item, view = 'main', onGenerate, onSave, onExport, generating = false }) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [imageError, setImageError] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  const handleGenerate = async () => {
    setIsGenerating(true)
    try {
      await onGenerate(item.id)
    } finally {
      setIsGenerating(false)
    }
  }

  // Для view='ai' item - это UserGeneration с вложенным catalog_item
  // Для view='main' item - это CatalogItem
  const displayItem = view === 'ai' && item.catalog_item ? item.catalog_item : item
  const rawImageUrl = displayItem.photoUrl || displayItem.photo_url || ''
  const imageUrl = rawImageUrl
  const generationId = item.id
  const [editedDescription, setEditedDescription] = useState(item.ai_description || '')
  const [editedKeywords, setEditedKeywords] = useState(item.ai_keywords || '')

  const handleSaveGeneration = async () => {
    if (!onSave || !generationId) {
      return
    }

    setIsSaving(true)
    try {
      await onSave(generationId, {
        ai_description: editedDescription,
        ai_keywords: editedKeywords
      })
      setIsEditing(false)
    } finally {
      setIsSaving(false)
    }
  }

  // Определяем статус для бейджа
  const getStatusBadge = () => {
    if (view === 'ai') {
      if (generating || isGenerating) {
        return { text: '● Обработка ИИ', className: 'status-wait' }
      }
      if (item.ai_description) {
        return { text: '● Готово', className: 'status-done' }
      }
      return { text: '● Обработка ИИ', className: 'status-wait' }
    }
    return null
  }

  const statusBadge = getStatusBadge()

  return (
    <div className="product-card">
      <div className="card-image">
        {!imageError && imageUrl ? (
          <img
            src={imageUrl}
            alt={displayItem.name || 'Фото товара'}
            className="card-image-img"
            loading="lazy"
            onError={() => setImageError(true)}
          />
        ) : (
          <svg className="card-image-placeholder" viewBox="0 0 24 24" fill="rgba(255,255,255,0.1)">
            <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
          </svg>
        )}
        {statusBadge && (
          <span className={`status-badge ${statusBadge.className}`}>
            {statusBadge.text}
          </span>
        )}
      </div>
      <div className="card-body">
        <div className="product-name">{displayItem.name}</div>
        <div className="product-price">
          {displayItem.price ? `${displayItem.price} ₽` : ''}
        </div>

        {view === 'ai' && (
          <div className="ai-info-block">
            {!isEditing ? (
              <>
                <div className="ai-info-row">
                  <span className="ai-info-label">Описание ИИ:</span>
                  <p className="ai-info-text">{item.ai_description || 'Нет описания'}</p>
                </div>
                <div className="ai-info-row">
                  <span className="ai-info-label">Ключевые слова:</span>
                  <p className="ai-info-text">{item.ai_keywords || 'Нет ключевых слов'}</p>
                </div>
              </>
            ) : (
              <>
                <div className="ai-info-row">
                  <span className="ai-info-label">Описание ИИ:</span>
                  <textarea
                    className="ai-edit-textarea"
                    value={editedDescription}
                    onChange={(e) => setEditedDescription(e.target.value)}
                    rows={4}
                  />
                </div>
                <div className="ai-info-row">
                  <span className="ai-info-label">Ключевые слова:</span>
                  <textarea
                    className="ai-edit-textarea"
                    value={editedKeywords}
                    onChange={(e) => setEditedKeywords(e.target.value)}
                    rows={3}
                  />
                </div>
              </>
            )}
          </div>
        )}

        <div className="card-actions">
          {view === 'ai' ? (
            <>
              {!isEditing ? (
                <button className="btn-card" data-tooltip="Редактировать описание" onClick={() => setIsEditing(true)}>
                  Редактировать
                </button>
              ) : (
                <button className="btn-card" onClick={handleSaveGeneration} disabled={isSaving}>
                  {isSaving ? 'Сохранение...' : 'Сохранить'}
                </button>
              )}
              {!isEditing ? (
                <button className="btn-card primary" onClick={onExport}>Download item</button>
              ) : (
                <button className="btn-card primary" onClick={() => setIsEditing(false)}>
                  Отмена
                </button>
              )}
            </>
          ) : (
            <>
              <button className="btn-card">Просмотр</button>
              <button
                className="btn-card primary"
                onClick={handleGenerate}
                disabled={isGenerating || item.generated}
              >
                {isGenerating ? 'Обработка...' : 'Генерировать'}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
