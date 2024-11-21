class Config:
    DB_URL = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    JWT_SECRET = "secret_key"  # Секретний ключ для токенів
    JWT_ALGORITHM = "HS256"  # Алгоритм шифрування токенів
    JWT_EXPIRATION_SECONDS = 3600  # Час дії токена (1 година)


config = Config
