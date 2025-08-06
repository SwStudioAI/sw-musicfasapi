#!/usr/bin/env python3
"""
Script de inicio simple para Cloud Run.
"""
import os
import sys

# Agregar el directorio de la app al path
sys.path.insert(0, '/app')

def main():
    """Función principal de inicio."""
    print("🚀 Starting SW Music FastAPI...")
    
    # Configurar el puerto desde la variable de entorno
    port = int(os.environ.get("PORT", 8000))
    
    try:
        import uvicorn
        from app.main import app
        
        print(f"🌐 Starting Uvicorn server on port {port}...")
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port, 
            workers=1,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
