#!/usr/bin/env python3
"""
Script para generar claves seguras para el proyecto FastAPI
"""

import secrets
import string

def generate_secret_key(length=32):
    """Genera una clave secreta URL-safe"""
    return secrets.token_urlsafe(length)

def generate_password(length=16):
    """Genera una contraseña segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("🔐 Generador de Credenciales Seguras")
    print("=" * 40)
    
    print(f"SECRET_KEY={generate_secret_key()}")
    print(f"FIRST_SUPERUSER_PASSWORD={generate_password()}")
    print(f"POSTGRES_PASSWORD={generate_password()}")
    
    print("\n💡 Copia estas credenciales a tu archivo .env")
    print("⚠️  ¡Guárdalas en un lugar seguro!")
