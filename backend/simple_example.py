#!/usr/bin/env python3
"""
Ejemplo simple usando Google Cloud AI Platform
"""

import asyncio
import os
from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel

# Configurar variables de entorno si no están definidas
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "sw-musicfastapi")

async def main():
    """Función principal con ejemplo de generación de texto"""
    try:
        # Inicializar AI Platform
        aiplatform.init(project="sw-musicfastapi", location="us-central1")
        
        # Usar el modelo de generación de texto
        model = TextGenerationModel.from_pretrained("text-bison")
        
        # Generar intro de radio
        response = model.predict(
            prompt="Escribe un intro de radio en español para un programa de música pop",
            temperature=0.7,
            max_output_tokens=256,
            top_p=0.8,
            top_k=40
        )
        
        print("🎵 Intro de radio generado:")
        print("=" * 50)
        print(response.text)
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Asegúrate de que:")
        print("   - Google Cloud CLI esté instalado")
        print("   - Estés autenticado: gcloud auth application-default login")
        print("   - El proyecto 'sw-musicfastapi' exista en Google Cloud")
        print("   - Las APIs estén habilitadas")

if __name__ == "__main__":
    asyncio.run(main())
