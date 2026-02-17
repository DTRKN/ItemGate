import '@testing-library/jest-dom'

declare const vi: any
declare const beforeAll: (fn: () => void) => void
declare const afterAll: (fn: () => void) => void

// Mock для fetch API
vi.stubGlobal('fetch', vi.fn())

// Mock для localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
vi.stubGlobal('localStorage', localStorageMock)

// Mock для console методов в тестах
const originalConsole = globalThis.console
beforeAll(() => {
  globalThis.console = {
    ...originalConsole,
    log: vi.fn(),
    warn: vi.fn(),
    error: vi.fn(),
  }
})

afterAll(() => {
  globalThis.console = originalConsole
})