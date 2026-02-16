export default function ItemTabs({ activeTab, onTabChange }) {
  return (
    <div className="tabs">
      <button 
        className={`tab-btn ${activeTab === 'copy' ? 'active' : ''}`}
        onClick={() => onTabChange('copy')}
      >
        Копирование
      </button>
      <button 
        className={`tab-btn ${activeTab === 'edit' ? 'active' : ''}`}
        onClick={() => onTabChange('edit')}
      >
        Редактирование
      </button>
    </div>
  )
}
