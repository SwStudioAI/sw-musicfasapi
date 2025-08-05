# SW Music FastAPI - Google Cloud Setup

Este proyecto incluye integración completa con Google Cloud AI Platform y Vertex AI para generación de contenido musical usando inteligencia artificial.

## 🚀 Deploy en Google Cloud Console

### 1. Preparación del Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/SwStudioAI/sw-musicfasapi.git
cd sw-musicfasapi

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### 2. Configuración en Google Cloud Console

1. **Crear/Seleccionar Proyecto:**
   - Ve a [Google Cloud Console](https://console.cloud.google.com)
   - Crea un nuevo proyecto o selecciona `sw-musicfasapi`
   - Anota el PROJECT_ID

2. **Habilitar APIs necesarias:**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable firebasevertexai.googleapis.com
   ```

3. **Configurar autenticación:**
   ```bash
   gcloud auth application-default login
   ```

### 3. Variables de Entorno Requeridas

```env
# Google Cloud / Vertex AI
GOOGLE_CLOUD_PROJECT=tu-project-id
GOOGLE_CLOUD_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-2.5-flash-lite

# Google APIs
GOOGLE_API_KEY=tu-api-key
GOOGLE_CLIENT_ID=tu-client-id
GOOGLE_CLIENT_SECRET=tu-client-secret
```

### 4. Deploy con Cloud Run

```bash
# Construir la imagen
docker build -t gcr.io/tu-project-id/sw-music-backend ./backend

# Subir a Container Registry
docker push gcr.io/tu-project-id/sw-music-backend

# Deploy en Cloud Run
gcloud run deploy sw-music-api \
  --image gcr.io/tu-project-id/sw-music-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=tu-project-id,GOOGLE_CLOUD_LOCATION=us-central1"
```

### 5. Deploy con App Engine

```bash
cd backend
gcloud app deploy
```

## 🎵 Funcionalidades de AI

### Endpoints Disponibles

- **POST** `/api/v1/google-ai/generate-text` - Generación de texto general
- **POST** `/api/v1/google-ai/generate-music-intro` - Intros musicales
- **POST** `/api/v1/google-ai/analyze-preferences` - Análisis de preferencias
- **GET** `/api/v1/google-ai/health` - Estado del servicio

### Ejemplos de Uso

```python
import requests

# Generar intro musical
response = requests.post("https://tu-app.run.app/api/v1/google-ai/generate-music-intro", 
    json={
        "style": "radio",
        "genre": "rock",
        "language": "español",
        "duration": "30 segundos"
    })

print(response.json()["content"])
```

## 🔧 Desarrollo Local

```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# Configurar base de datos
alembic upgrade head

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentación

- API Docs: `http://localhost:8000/docs`
- Configuración detallada: `backend/GOOGLE_CLOUD_SETUP.md`
- Tests: `backend/test_google_ai.py`

## 🌟 Características

✅ Integración con Vertex AI y Google Cloud AI Platform  
✅ Generación de contenido musical con IA  
✅ Análisis de preferencias musicales  
✅ Autenticación Google OAuth  
✅ API REST completamente documentada  
✅ Deploy ready para Google Cloud  
✅ Docker support  
✅ Tests automatizados  

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
