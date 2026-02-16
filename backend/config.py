import os
import dotenv

dotenv.load_dotenv()

class Config:
    DB_NAME = os.getenv("DB_NAME", "itemgate")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    AI_KEY = os.getenv("AI_KEY")
    USE_POSTGRES = os.getenv("USE_POSTGRES", "false").lower() == "true"
    prompt_system_generate_info: str = "prompts/info_for_seller.yaml"

    @property
    def database_url(self) -> str:
        if self.USE_POSTGRES:
            # PostgreSQL для Docker/Production
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            # SQLite для локальной разработки
            return f"sqlite+aiosqlite:///./{self.DB_NAME}_database.db"

config = Config()
