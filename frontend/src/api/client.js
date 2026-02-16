const API_BASE = 'http://localhost:8000'

// Управление токеном
const TOKEN_KEY = 'auth_token'

export const authService = {
  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  },
  
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token)
  },
  
  removeToken() {
    localStorage.removeItem(TOKEN_KEY)
  },
  
  isAuthenticated() {
    return !!this.getToken()
  }
}

// Получение заголовков с токеном
function getHeaders(includeAuth = true) {
  const headers = { 'Content-Type': 'application/json' }
  if (includeAuth) {
    const token = authService.getToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
  }
  return headers
}

export const apiClient = {
  // === AUTHENTICATION ===
  async register(email, password, fullName = null) {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: getHeaders(false),
      body: JSON.stringify({ email, password, full_name: fullName }),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }
    return response.json()
  },

  async login(email, password) {
    const response = await fetch(`${API_BASE}/auth/login-json`, {
      method: 'POST',
      headers: getHeaders(false),
      body: JSON.stringify({ email, password }),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }
    const data = await response.json()
    authService.setToken(data.access_token)
    return data
  },

  async getMe() {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: getHeaders(),
    })
    if (!response.ok) {
      if (response.status === 401) {
        authService.removeToken()
      }
      throw new Error('Failed to get user info')
    }
    return response.json()
  },

  logout() {
    authService.removeToken()
  },

  // === ITEMS ===
  async getItems() {
    const response = await fetch(`${API_BASE}/sima-land/get_items`, {
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch items')
    return response.json()
  },

  async getItemsSellers() {
    const response = await fetch(`${API_BASE}/sima-land/get_items_sellers`, {
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch AI items')
    return response.json()
  },

  async generateDescription(id_item) {
    const response = await fetch(
      `${API_BASE}/sima-land/ai_generate_desc_seller/${id_item}`,
      { 
        method: 'POST',
        headers: getHeaders(),
      }
    )
    if (!response.ok) throw new Error('Failed to generate description')
    return response.json()
  },

  async searchItems(word) {
    const response = await fetch(
      `${API_BASE}/sima-land/search_item_to_word/${word}`,
      { 
        method: 'POST',
        headers: getHeaders(),
      }
    )
    if (!response.ok) throw new Error('Failed to search items')
    return response.json()
  },

  async searchGeneratedItems(word) {
    const response = await fetch(
      `${API_BASE}/sima-land/search_generated_items/${word}`,
      {
        method: 'POST',
        headers: getHeaders(),
      }
    )
    if (!response.ok) throw new Error('Failed to search generated items')
    return response.json()
  },

  async updateItem(generation_id, payload) {
    const response = await fetch(`${API_BASE}/sima-land/update_generation/${generation_id}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    })
    if (!response.ok) throw new Error('Failed to update generation')
    return response.json()
  },

  // === ADMIN ONLY ===
  async loadItems(count) {
    const token = authService.getToken()
    return new EventSource(`${API_BASE}/sima-land/loading_words_db/${count}?token=${token}`)
  },

  async getLogs() {
    const response = await fetch(`${API_BASE}/sima-land/logs`, {
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch logs')
    return response.json()
  },

  // === EXCEL ===
  async uploadExcel(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    const token = authService.getToken()
    const response = await fetch(`${API_BASE}/excel/upload-items`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData,
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to upload Excel')
    }
    return response.json()
  },

  async downloadBackup() {
    const token = authService.getToken()
    const response = await fetch(`${API_BASE}/excel/backup-database`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
    })
    if (!response.ok) throw new Error('Failed to download backup')
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `itemgate_backup_${new Date().toISOString().split('T')[0]}.xlsx`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  },

  async exportItems() {
    const token = authService.getToken()
    const response = await fetch(`${API_BASE}/excel/export-items`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
    })
    if (!response.ok) throw new Error('Failed to export items')
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `items_export_${new Date().toISOString().split('T')[0]}.xlsx`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  }
}
