from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.sima_land import router as sima_land_router
from routers.auth import router as auth_router
from routers.excel import router as excel_router
from services.logger import log_info, log_error
import time

app = FastAPI(title="ItemGate API", version="0.1.0")

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Логируем входящий запрос
    log_info(f"Запрос: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Логируем успешный ответ
        log_info(
            f"Ответ: {request.method} {request.url.path} | "
            f"Статус: {response.status_code} | Время: {process_time:.3f}с"
        )
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        log_error(
            f"Ошибка: {request.method} {request.url.path} | "
            f"Время: {process_time:.3f}с | Ошибка: {str(e)}",
            exc_info=True
        )
        raise

# CORS middleware для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1",
        "http://127.0.0.1:80",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sima_land_router, prefix="/sima-land", tags=["Sima-Land"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(excel_router, tags=["Excel"])

@app.get('/')
async def health_check():
    log_info("Health check called")
    return {"status": "ok", "service": "ItemGate API"}

@app.get('/health')
async def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    log_info("🚀 ItemGate API запущен")

@app.on_event("shutdown")
async def shutdown_event():
    log_info("🛑 ItemGate API остановлен")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
