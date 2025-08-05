#!/bin/bash

# Script de deploy automático para Google Cloud
# Uso: ./deploy.sh [PROJECT_ID]

set -e

# Configuración
PROJECT_ID=${1:-"sw-musicfasapi"}
REGION="us-central1"
SERVICE_NAME="sw-music-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/sw-music-backend"

echo "🚀 Iniciando deploy de SW Music FastAPI..."
echo "📁 Proyecto: ${PROJECT_ID}"
echo "🌍 Región: ${REGION}"
echo "🏷️  Imagen: ${IMAGE_NAME}"

# Verificar que estamos logueados
echo "🔐 Verificando autenticación..."
gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1
if [ $? -ne 0 ]; then
    echo "❌ No hay sesión activa en gcloud. Ejecuta: gcloud auth login"
    exit 1
fi

# Configurar proyecto
echo "⚙️  Configurando proyecto..."
gcloud config set project ${PROJECT_ID}

# Habilitar APIs necesarias
echo "🔧 Habilitando APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable firebasevertexai.googleapis.com

# Construir imagen
echo "🏗️  Construyendo imagen Docker..."
cd backend
gcloud builds submit --tag ${IMAGE_NAME} .

# Deploy a Cloud Run
echo "☁️  Desplegando en Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8000 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --min-instances 0 \
    --timeout 300s \
    --set-env-vars "ENVIRONMENT=production,GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${REGION},VERTEX_AI_MODEL=gemini-2.5-flash-lite"

# Obtener URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)')

echo "✅ Deploy completado!"
echo "🌐 URL del servicio: ${SERVICE_URL}"
echo "📖 Documentación: ${SERVICE_URL}/docs"
echo "🔍 Health check: ${SERVICE_URL}/api/v1/google-ai/health"

# Opcional: Configurar dominio personalizado
read -p "¿Quieres configurar un dominio personalizado? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Ingresa el dominio (ej: api.sw-music.com): " DOMAIN
    echo "🔗 Configurando dominio personalizado..."
    gcloud run domain-mappings create --service ${SERVICE_NAME} --domain ${DOMAIN} --region ${REGION}
    echo "📋 Configura estos registros DNS:"
    gcloud run domain-mappings describe ${DOMAIN} --region ${REGION} --format='value(status.resourceRecords[].rrdata)'
fi

echo "🎉 Deploy finalizado con éxito!"
