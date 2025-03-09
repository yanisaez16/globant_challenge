from google.cloud.sql.connector import Connector
import sqlalchemy
import os

# Crear el conector de Cloud SQL
connector = Connector()

# Intentar la conexión
try:
    print("Intentando conectar a Cloud SQL...")
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=lambda: connector.connect(
            os.getenv("INSTANCE_CONNECTION_NAME"),
            "pg8000",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )

    with engine.connect() as conn:
        print("✅ Conexión exitosa a Cloud SQL")
        result = conn.execute(sqlalchemy.text("SELECT NOW();"))
        print("Hora del servidor:", result.fetchone()[0])

except Exception as e:
    print("❌ Error al conectar a Cloud SQL:", e)
