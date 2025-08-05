#!/usr/bin/env python3
"""
Script de prueba para Google Cloud AI Platform
"""

import asyncio
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.google_ai import get_google_ai_service


async def test_google_cloud_ai():
    """Prueba la integración con Google Cloud AI Platform"""
    print("🤖 Probando Google Cloud AI Platform...")
    print("=" * 50)
    
    try:
        service = get_google_ai_service()
        
        # Verificar estado del servicio
        status = await service.get_service_status()
        print(f"📊 Estado del servicio:")
        print(f"   Inicializado: {status['initialized']}")
        print(f"   Proyecto: {status['project_id']}")
        print(f"   Región: {status['location']}")
        print(f"   Modelos disponibles: {', '.join(status['available_models'])}")
        
        if not status['initialized']:
            print("\n❌ Servicio no inicializado. Verifica:")
            print("   - Google Cloud CLI instalado y autenticado")
            print("   - Proyecto configurado en .env")
            print("   - APIs habilitadas en Google Cloud")
            return
        
        print("\n🧪 Prueba 1: Conexión básica")
        test_response = await service.test_connection()
        print(f"✅ Respuesta: {test_response}")
        
        print("\n🧪 Prueba 2: Generar intro de radio (text-bison)")
        intro = await service.generate_music_intro(
            style="radio",
            genre="pop latino",
            language="español",
            duration="30 segundos"
        )
        print("✅ Intro generado:")
        print("-" * 40)
        print(intro)
        print("-" * 40)
        
        print("\n🧪 Prueba 3: Generación con Gemini Pro")
        gemini_response = await service.generate_text_with_gemini(
            prompt="Escribe un breve texto sobre la importancia de la música en la vida diaria",
            temperature=0.7,
            max_output_tokens=300
        )
        print("✅ Respuesta de Gemini:")
        print("-" * 40)
        print(gemini_response)
        print("-" * 40)
        
        print("\n🧪 Prueba 4: Análisis de preferencias musicales")
        user_data = {
            "generos_favoritos": ["pop", "rock", "electrónica"],
            "artistas_recientes": ["Dua Lipa", "The Weeknd", "Billie Eilish"],
            "mood_preferido": "energético",
            "horario_escucha": "tarde-noche"
        }
        
        analysis = await service.analyze_music_preferences(user_data)
        print("✅ Análisis de preferencias:")
        print("-" * 40)
        print(analysis)
        print("-" * 40)
        
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Ejecuta: gcloud auth application-default login")
        print("   2. Verifica que el proyecto esté configurado: gcloud config set project sw-musicfastapi")
        print("   3. Habilita las APIs necesarias en Google Cloud Console")


async def test_specific_example():
    """Prueba el ejemplo específico que mencionaste"""
    print("\n🎵 Probando ejemplo específico: Intro de radio")
    print("=" * 50)
    
    try:
        service = get_google_ai_service()
        
        # Tu ejemplo adaptado
        prompt = "Escribe un intro de radio en español"
        response = await service.generate_text_with_bison(
            prompt=prompt,
            temperature=0.8,
            max_output_tokens=256
        )
        
        print("✅ Intro de radio generado:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 Iniciando pruebas de Google Cloud AI Platform...")
    asyncio.run(test_google_cloud_ai())
    asyncio.run(test_specific_example())
