#!/usr/bin/env python3
"""
Script de prueba para Vertex AI
"""

import asyncio
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vertex_ai import vertex_ai_service


async def test_vertex_ai():
    """Prueba básica de Vertex AI"""
    print("🤖 Probando integración con Vertex AI...")
    
    try:
        # Prueba de generación de contenido
        prompt = "Hola, ¿puedes generar una breve descripción sobre música electrónica?"
        print(f"📝 Prompt: {prompt}")
        print("🔄 Generando respuesta...")
        
        response = await vertex_ai_service.generate_content(
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=500
        )
        
        print("✅ Respuesta generada:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que:")
        print("   - Las credenciales de Google Cloud estén configuradas")
        print("   - El proyecto 'sw-musicfasapi' exista en Google Cloud")
        print("   - La API de Vertex AI esté habilitada")


async def test_streaming():
    """Prueba de generación streaming"""
    print("\n🌊 Probando generación streaming...")
    
    try:
        prompt = "Explica qué es el jazz en 3 párrafos"
        print(f"📝 Prompt: {prompt}")
        print("🔄 Generando respuesta en streaming...")
        print("-" * 50)
        
        async for chunk in vertex_ai_service.generate_content_stream(
            prompt=prompt,
            temperature=0.5,
            max_output_tokens=800
        ):
            print(chunk, end="", flush=True)
        
        print("\n" + "-" * 50)
        print("✅ Streaming completado")
        
    except Exception as e:
        print(f"❌ Error en streaming: {e}")


if __name__ == "__main__":
    asyncio.run(test_vertex_ai())
    asyncio.run(test_streaming())
