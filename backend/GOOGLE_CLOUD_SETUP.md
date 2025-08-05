# 🔐 Configuración Manual de Google Cloud

Si prefieres configurar Google Cloud manualmente, sigue estos pasos:

## 📋 Requisitos Previos

1. **Cuenta de Google Cloud**: Necesitas una cuenta activa
2. **Proyecto de Google Cloud**: Crea o usa un proyecto existente
3. **Facturación habilitada**: Vertex AI requiere facturación activa

## 🛠️ Pasos de Configuración

### 1. Instalar Google Cloud CLI

**Windows:**
```powershell
# Opción 1: Descargar desde el sitio web
# Ve a: https://cloud.google.com/sdk/docs/install

# Opción 2: Con Chocolatey
choco install gcloudsdk

# Opción 3: Con Scoop
scoop bucket add extras
scoop install gcloud
```

### 2. Autenticación

```bash
# Autenticación principal
gcloud auth login

# Credenciales para aplicaciones
gcloud auth application-default login
```

### 3. Configurar Proyecto

```bash
# Crear proyecto (si no existe)
gcloud projects create sw-musicfasapi

# Configurar proyecto por defecto
gcloud config set project sw-musicfasapi

# Verificar configuración
gcloud config list
```

### 4. Habilitar APIs

```bash
# APIs necesarias para Vertex AI
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativeai.googleapis.com
gcloud services enable storage.googleapis.com

# Verificar APIs habilitadas
gcloud services list --enabled
```

### 5. Configurar Variables de Entorno

Actualiza tu archivo `.env`:

```properties
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=sw-musicfasapi
GOOGLE_CLOUD_LOCATION=global
VERTEX_AI_MODEL=gemini-2.5-flash-lite

# Google API Key (opcional para APIs públicas)
GOOGLE_API_KEY=tu_api_key_aqui

# Google OAuth (para autenticación de usuarios)
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret
GOOGLE_REDIRECT_URI=https://tu-dominio.com/auth/google/callback
```

### 6. Configurar Credenciales (Métodos)

#### Método 1: Credenciales por Defecto (Recomendado para desarrollo)
```bash
gcloud auth application-default login
```

#### Método 2: Service Account (Recomendado para producción)
```bash
# Crear service account
gcloud iam service-accounts create vertex-ai-service \
    --display-name="Vertex AI Service Account"

# Asignar roles
gcloud projects add-iam-policy-binding sw-musicfasapi \
    --member="serviceAccount:vertex-ai-service@sw-musicfasapi.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Crear y descargar key
gcloud iam service-accounts keys create vertex-ai-key.json \
    --iam-account=vertex-ai-service@sw-musicfasapi.iam.gserviceaccount.com

# Configurar variable de entorno
set GOOGLE_APPLICATION_CREDENTIALS=path\to\vertex-ai-key.json
```

#### Método 3: Variable de Entorno en .env
```properties
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
```

## 🧪 Verificar Configuración

### 1. Verificar autenticación
```bash
gcloud auth list
```

### 2. Verificar proyecto
```bash
gcloud config get-value project
```

### 3. Probar Vertex AI
```bash
# Desde el directorio backend
python test_vertex_ai.py
```

### 4. Probar API FastAPI
```bash
# Iniciar servidor
python run_dev.py

# Probar endpoint
curl -X GET "http://localhost:8000/api/v1/ai/vertex-ai/status" \
  -H "Authorization: Bearer tu_token_jwt"
```

## 🔧 Solución de Problemas

### Error: "No module named 'google'"
```bash
# Instalar dependencias
pip install google-genai google-cloud-aiplatform google-auth
```

### Error: "DefaultCredentialsError"
```bash
# Re-autenticar
gcloud auth application-default login
```

### Error: "Project not found"
```bash
# Verificar proyecto existe
gcloud projects describe sw-musicfasapi

# Crear si no existe
gcloud projects create sw-musicfasapi
```

### Error: "API not enabled"
```bash
# Habilitar APIs manualmente
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativeai.googleapis.com
```

## 📊 Monitoreo y Costos

### Ver uso de Vertex AI
```bash
# Ver cuotas
gcloud compute project-info describe --project=sw-musicfasapi

# Monitorear en Console
https://console.cloud.google.com/ai-platform/
```

### Configurar alertas de facturación
1. Ve a Google Cloud Console
2. Facturación > Presupuestos y alertas
3. Crea alertas para controlar costos

## 🚀 Próximos Pasos

1. **Prueba la configuración** con el script de prueba
2. **Implementa funciones personalizadas** en el servicio Vertex AI
3. **Configura monitoreo** y alertas de costos
4. **Despliega en producción** con service accounts

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de la aplicación
2. Verifica la documentación oficial: https://cloud.google.com/vertex-ai/docs
3. Usa el foro de la comunidad: https://stackoverflow.com/questions/tagged/google-cloud-vertex-ai
