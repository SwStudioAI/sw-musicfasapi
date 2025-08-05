"""
API routes para integración con Vertex AI
"""

from typing import Any
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.api.deps import CurrentUser
from app.services.vertex_ai import get_vertex_ai_service

router = APIRouter()


class GenerateContentRequest(BaseModel):
    """Modelo para solicitudes de generación de contenido"""
    prompt: str
    temperature: float = 1.0
    top_p: float = 0.95
    max_output_tokens: int = 65535


class MusicRecommendationRequest(BaseModel):
    """Modelo para solicitudes de recomendaciones musicales"""
    user_preferences: dict
    listening_history: list


class GenerateContentResponse(BaseModel):
    """Modelo para respuestas de generación de contenido"""
    content: str
    success: bool
    message: str = ""


@router.post("/generate-content", response_model=GenerateContentResponse)
async def generate_content(
    request: GenerateContentRequest,
    current_user: CurrentUser,
) -> Any:
    """
    Genera contenido usando Vertex AI
    """
    try:
        service = get_vertex_ai_service()
        content = await service.generate_content(
            prompt=request.prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            max_output_tokens=request.max_output_tokens
        )
        
        return GenerateContentResponse(
            content=content,
            success=True,
            message="Contenido generado exitosamente"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando contenido: {str(e)}"
        )


@router.post("/analyze-music")
async def analyze_music(
    current_user: CurrentUser,
    audio_file: UploadFile = File(...),
) -> Any:
    """
    Analiza un archivo de audio usando Vertex AI
    """
    try:
        # Validar tipo de archivo
        if not audio_file.content_type or not audio_file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=400,
                detail="El archivo debe ser un audio válido"
            )
        
        # Leer datos del archivo
        audio_data = await audio_file.read()
        
        # Analizar con Vertex AI
        service = get_vertex_ai_service()
        analysis = await service.generate_music_analysis(audio_data)
        
        return {
            "analysis": analysis,
            "filename": audio_file.filename,
            "content_type": audio_file.content_type,
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analizando audio: {str(e)}"
        )


@router.post("/music-recommendations")
async def get_music_recommendations(
    request: MusicRecommendationRequest,
    current_user: CurrentUser,
) -> Any:
    """
    Genera recomendaciones musicales personalizadas
    """
    try:
        service = get_vertex_ai_service()
        recommendations = await service.generate_music_recommendation(
            user_preferences=request.user_preferences,
            listening_history=request.listening_history
        )
        
        return {
            "recommendations": recommendations,
            "user_id": current_user.id,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando recomendaciones: {str(e)}"
        )


@router.get("/vertex-ai/status")
async def vertex_ai_status(current_user: CurrentUser) -> Any:
    """
    Verifica el estado de la conexión con Vertex AI
    """
    try:
        # Test simple de conexión
        service = get_vertex_ai_service()
        test_response = await service.generate_content(
            prompt="Responde con 'OK' si me puedes escuchar.",
            max_output_tokens=10
        )
        
        return {
            "status": "connected",
            "model": service.model,
            "test_response": test_response,
            "success": True
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "success": False
        }
