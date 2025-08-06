#!/usr/bin/env python3
"""
Script de inicio para Cloud Run con verificación de base de datos.
"""
import time
import sys
from sqlmodel import Session, select
import uvicorn

def wait_for_database():
    """Espera a que la base de datos esté disponible."""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            from app.core.db import engine
            with Session(engine) as session:
                session.exec(select(1))
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            retry_count += 1
            print(f"⏳ Database connection attempt {retry_count}/{max_retries} failed: {e}")
            if retry_count >= max_retries:
                print("⚠️ Starting server without database verification...")
                return False
            time.sleep(2)
    
    return False

def main():
    """Función principal de inicio."""
    print("🚀 Starting SW Music FastAPI...")
    
    # Intentar conectar a la base de datos
    wait_for_database()
    
    # Iniciar el servidor
    print("🌐 Starting Uvicorn server...")
    from app.main import app
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        workers=1,
        log_level="info"
    )

if __name__ == "__main__":
    main()
