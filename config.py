
POSTGRES_USER = "calendar"
POSTGRES_PASSWORD = "calendar"
POSTGRES_HOST = "localhost"
# POSTGRES_HOST = "calendar_postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "calendar"

SQLALCHEMY_POSTGRES_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"