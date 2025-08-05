#!/usr/bin/env python3
"""
Script para configurar credenciales de Google Cloud
"""

import os
import subprocess
import sys
import json
from pathlib import Path


def check_gcloud_cli():
    """Verifica si Google Cloud CLI está instalado"""
    try:
        result = subprocess.run(['gcloud', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Google Cloud CLI encontrado")
            print(result.stdout.split('\n')[0])
            return True
        else:
            print("❌ Google Cloud CLI no encontrado")
            return False
    except FileNotFoundError:
        print("❌ Google Cloud CLI no está instalado")
        return False


def install_gcloud_cli():
    """Instrucciones para instalar Google Cloud CLI"""
    print("\n📦 Para instalar Google Cloud CLI:")
    print("1. Ve a: https://cloud.google.com/sdk/docs/install")
    print("2. Descarga e instala Google Cloud CLI para Windows")
    print("3. Reinicia tu terminal después de la instalación")
    print("4. Ejecuta este script nuevamente")


def check_authentication():
    """Verifica si está autenticado con Google Cloud"""
    try:
        result = subprocess.run(['gcloud', 'auth', 'list'], capture_output=True, text=True)
        if result.returncode == 0 and 'ACTIVE' in result.stdout:
            print("✅ Autenticado con Google Cloud")
            # Mostrar cuenta activa
            lines = result.stdout.split('\n')
            for line in lines:
                if 'ACTIVE' in line:
                    print(f"   Cuenta activa: {line.strip()}")
            return True
        else:
            print("❌ No autenticado con Google Cloud")
            return False
    except Exception as e:
        print(f"❌ Error verificando autenticación: {e}")
        return False


def authenticate():
    """Autentica con Google Cloud"""
    print("\n🔐 Iniciando proceso de autenticación...")
    try:
        # Autenticación principal
        result = subprocess.run(['gcloud', 'auth', 'login'], check=True)
        
        # Configurar credenciales por defecto para aplicaciones
        print("\n🔑 Configurando credenciales para aplicaciones...")
        result = subprocess.run(['gcloud', 'auth', 'application-default', 'login'], check=True)
        
        print("✅ Autenticación completada")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en autenticación: {e}")
        return False


def set_project(project_id="sw-musicfasapi"):
    """Configura el proyecto de Google Cloud"""
    print(f"\n🏗️ Configurando proyecto: {project_id}")
    try:
        # Verificar si el proyecto existe
        result = subprocess.run(
            ['gcloud', 'projects', 'describe', project_id], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Proyecto {project_id} encontrado")
        else:
            print(f"❌ Proyecto {project_id} no encontrado")
            create_project = input(f"¿Quieres crear el proyecto {project_id}? (y/n): ")
            if create_project.lower() == 'y':
                subprocess.run(['gcloud', 'projects', 'create', project_id], check=True)
                print(f"✅ Proyecto {project_id} creado")
            else:
                return False
        
        # Configurar como proyecto por defecto
        subprocess.run(['gcloud', 'config', 'set', 'project', project_id], check=True)
        print(f"✅ Proyecto {project_id} configurado como predeterminado")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configurando proyecto: {e}")
        return False


def enable_apis():
    """Habilita las APIs necesarias"""
    apis = [
        'aiplatform.googleapis.com',
        'generativeai.googleapis.com',
        'storage.googleapis.com'
    ]
    
    print("\n🔌 Habilitando APIs necesarias...")
    for api in apis:
        try:
            print(f"   Habilitando {api}...")
            subprocess.run(['gcloud', 'services', 'enable', api], check=True)
            print(f"   ✅ {api} habilitada")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error habilitando {api}: {e}")


def check_credentials_file():
    """Verifica si existe archivo de credenciales"""
    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if cred_path and os.path.exists(cred_path):
        print(f"✅ Archivo de credenciales encontrado: {cred_path}")
        return True
    else:
        print("ℹ️  Usando credenciales por defecto (gcloud auth application-default)")
        return True


def test_vertex_ai_connection():
    """Prueba la conexión con Vertex AI"""
    print("\n🧪 Probando conexión con Vertex AI...")
    try:
        # Cambiar al directorio del proyecto
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Ejecutar script de prueba
        result = subprocess.run([
            sys.executable, 'test_vertex_ai.py'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Conexión con Vertex AI exitosa")
            print("Respuesta:")
            print(result.stdout)
            return True
        else:
            print("❌ Error en conexión con Vertex AI")
            print("Error:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout en la prueba de conexión")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando prueba: {e}")
        return False


def main():
    """Función principal de configuración"""
    print("🚀 Configurador de Google Cloud para SW Music Fast API")
    print("=" * 60)
    
    # 1. Verificar Google Cloud CLI
    if not check_gcloud_cli():
        install_gcloud_cli()
        return
    
    # 2. Verificar autenticación
    if not check_authentication():
        if not authenticate():
            return
    
    # 3. Configurar proyecto
    project_id = input("\nIngresa el ID del proyecto de Google Cloud (default: sw-musicfasapi): ").strip()
    if not project_id:
        project_id = "sw-musicfasapi"
    
    if not set_project(project_id):
        return
    
    # 4. Habilitar APIs
    enable_apis()
    
    # 5. Verificar credenciales
    check_credentials_file()
    
    # 6. Probar conexión
    print("\n🔄 Configuración completada. Probando conexión...")
    if test_vertex_ai_connection():
        print("\n🎉 ¡Configuración exitosa!")
        print("Ya puedes usar Vertex AI en tu aplicación FastAPI")
    else:
        print("\n⚠️  Configuración completada pero la prueba falló")
        print("Revisa los logs para más detalles")


if __name__ == "__main__":
    main()
