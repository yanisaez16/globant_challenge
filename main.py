from fastapi import FastAPI
from google.cloud.sql.connector import Connector
import sqlalchemy
import os
from typing import List, Dict

# Crear una instancia de FastAPI
app = FastAPI()

# Configuración de conexión con SQLAlchemy
connector = Connector()

def get_db_connection():
    """Obtiene una conexión a la base de datos usando el conector de Cloud SQL"""
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=lambda: connector.connect(
            os.getenv("INSTANCE_CONNECTION_NAME"),  # challenge-de:southamerica-west1:my-database
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
    return engine.connect()

# Endpoint para empleados contratados por trimestre en 2021
@app.get("/employees-by-quarter", response_model=List[Dict[str, str]])
async def get_employees_by_quarter():
    query = """
    SELECT 
        d.department,
        j.job,
        COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime::TIMESTAMP) = 1) AS Q1,
        COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime::TIMESTAMP) = 2) AS Q2,
        COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime::TIMESTAMP) = 3) AS Q3,
        COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime::TIMESTAMP) = 4) AS Q4
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    JOIN jobs j ON he.job_id = j.id
    WHERE EXTRACT(YEAR FROM he.datetime::TIMESTAMP) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job;
    """
    
    with get_db_connection() as conn:
        result = conn.execute(sqlalchemy.text(query))
        rows = result.fetchall()

    return [
        {"department": row[0], "job": row[1], "Q1": str(row[2]), "Q2": str(row[3]), "Q3": str(row[4]), "Q4": str(row[5])}
        for row in rows
    ]

# Endpoint para departamentos con contrataciones sobre el promedio en 2021
@app.get("/departments-above-average", response_model=List[Dict[str, str]])
async def get_departments_above_average():
    query = """
    WITH department_hires AS (
        SELECT 
            he.department_id AS id,
            d.department,
            COUNT(*) AS hired
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        WHERE EXTRACT(YEAR FROM he.datetime::TIMESTAMP) = 2021
        GROUP BY he.department_id, d.department
    ),
    average_hires AS (
        SELECT AVG(hired) AS avg_hires FROM department_hires
    )
    SELECT 
        dh.id, 
        dh.department, 
        dh.hired
    FROM department_hires dh
    JOIN average_hires ah ON dh.hired > ah.avg_hires
    ORDER BY dh.hired DESC;
    """
    
    with get_db_connection() as conn:
        result = conn.execute(sqlalchemy.text(query))
        rows = result.fetchall()

    # Convertir los valores a cadena
    return [
        {"id": str(row[0]), "department": str(row[1]), "hired": str(row[2])}
        for row in rows
    ]

