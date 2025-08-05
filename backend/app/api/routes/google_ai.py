"""
API routes para Google Cloud AI Platform
"""

from typing import Any, List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.api.deps import CurrentUser
from app.services.google_ai import get_google_ai_service

router = APIRouter()


class GenerateTextRequest(BaseModel):
    """Modelo para solicitudes de generación de texto"""
    prompt: str
    model: str = "text-bison"  # text-bison o gemini-pro
    temperature: float = 0.7
    max_output_tokens: int = 1024
    top_p: float = 0.8
    top_k: int = 40


class MusicIntroRequest(BaseModel):
    """Modelo para solicitudes de intro musical"""
    style: str = "radio"
    genre: str = "pop"
    language: str = "español"
    duration: str = "30 segundos"


class PlaylistDescriptionRequest(BaseModel):
    """Modelo para solicitudes de descripción de playlist"""
    playlist_name: str
    songs: List[str]
    theme: str = ""


class AnalyzePreferencesRequest(BaseModel):
    """Modelo para análisis de preferencias musicales"""
    user_data: Dict[str, Any]


@router.post("/generate-text")
async def generate_text(
    request: GenerateTextRequest,
    current_user: CurrentUser,
) -> Any:
    """
    Genera texto usando Google Cloud AI Platform
    """
    try:
        service = get_google_ai_service()
        
        if request.model == "gemini-pro":
            content = await service.generate_text_with_gemini(
                prompt=request.prompt,
                temperature=request.temperature,
                max_output_tokens=request.max_output_tokens,
                top_p=request.top_p,
                top_k=request.top_k
            )
        else:  # text-bison por defecto
            content = await service.generate_text_with_bison(
                prompt=request.prompt,
                temperature=request.temperature,
                max_output_tokens=request.max_output_tokens,
                top_p=request.top_p,
                top_k=request.top_k
            )
        
        return {
            "content": content,
            "model_used": request.model,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando texto: {str(e)}"
        )


@router.post("/generate-music-intro")
async def generate_music_intro(
    request: MusicIntroRequest,
    current_user: CurrentUser,
) -> Any:
    """
    Genera un intro musical personalizado
    """
    try:
        service = get_google_ai_service()
        
        intro = await service.generate_music_intro(
            style=request.style,
            genre=request.genre,
            language=request.language,
            duration=request.duration
        )
        
        return {
            "intro": intro,
            "style": request.style,
            "genre": request.genre,
            "language": request.language,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando intro musical: {str(e)}"
        )


@router.post("/generate-playlist-description")
async def generate_playlist_description(
    request: PlaylistDescriptionRequest,
    current_user: CurrentUser,
) -> Any:
    """
    Genera descripción para una playlist
    """
    try:
        service = get_google_ai_service()
        
        description = await service.generate_playlist_description(
            playlist_name=request.playlist_name,
            songs=request.songs,
            theme=request.theme
        )
        
        return {
            "description": description,
            "playlist_name": request.playlist_name,
            "songs_count": len(request.songs),
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando descripción de playlist: {str(e)}"
        )


@router.post("/analyze-music-preferences")
async def analyze_music_preferences(
    request: AnalyzePreferencesRequest,
    current_user: CurrentUser,
) -> Any:
    """
    Analiza las preferencias musicales del usuario
    """
    try:
        service = get_google_ai_service()
        
        analysis = await service.analyze_music_preferences(
            user_data=request.user_data
        )
        
        return {
            "analysis": analysis,
            "user_id": current_user.id,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analizando preferencias: {str(e)}"
        )


@router.get("/service-status")
async def get_service_status(current_user: CurrentUser) -> Any:
    """
    Obtiene el estado del servicio Google Cloud AI
    """
    try:
        service = get_google_ai_service()
        status = await service.get_service_status()
        
        return {
            **status,
            "success": True
        }
        
    except Exception as e:
        return {
            "initialized": False,
            "error": str(e),
            "success": False
        }


@router.get("/test-connection")
async def test_connection(current_user: CurrentUser) -> Any:
    """
    Prueba la conexión con Google Cloud AI
    """
    try:
        service = get_google_ai_service()
        test_response = await service.test_connection()
        
        return {
            "status": "connected",
            "test_response": test_response,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en prueba de conexión: {str(e)}"
        )


# Endpoint especial para generar intro de radio (como en tu ejemplo)
@router.post("/radio-intro")
async def generate_radio_intro(
    current_user: CurrentUser,
    genre: str = "pop",
    program_name: str = "SW Music Radio"
) -> Any:
    """
    Genera un intro de radio en español (ejemplo específico)
    """
    try:
        service = get_google_ai_service()
        
        # Prompt específico para intro de radio
        prompt = f"""
        Escribe un intro de radio en español para un programa llamado "{program_name}" 
        que se especializa en música {genre}. 
        
        El intro debe:
        - Ser energético y profesional
        - Durar aproximadamente 30 segundos cuando se lea
        - Incluir el nombre del programa
        - Mencionar el género musical
        - Terminar con una frase que invite a seguir escuchando
        
        No uses asteriscos ni indicaciones de efectos sonoros.
        """
        
        intro = await service.generate_text_with_bison(
            prompt=prompt,
            temperature=0.8,
            max_output_tokens=256
        )
        
        return {
            "intro": intro,
            "program_name": program_name,
            "genre": genre,
            "language": "español",
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando intro de radio: {str(e)}"
        )


# Endpoint público para probar la conexión (sin autenticación)
@router.get("/health")
async def health_check() -> Any:
    """
    Verifica el estado del servicio Google Cloud AI sin autenticación
    """
    try:
        service = get_google_ai_service()
        status = await service.get_service_status()
        
        return {
            **status,
            "message": "Google Cloud AI service is running",
            "success": True
        }
        
    except Exception as e:
        return {
            "initialized": False,
            "error": str(e),
            "message": "Google Cloud AI service is not available",
            "success": False
        }


# Endpoint público para prueba simple de texto (sin autenticación)
@router.post("/test-text")
async def test_text_generation(request: GenerateTextRequest) -> Any:
    """
    Endpoint de prueba para generar texto sin autenticación
    """
    try:
        service = get_google_ai_service()
        
        if request.model == "gemini-pro":
            content = await service.generate_text_with_gemini(
                prompt=request.prompt,
                temperature=request.temperature,
                max_output_tokens=request.max_output_tokens,
                top_p=request.top_p,
                top_k=request.top_k
            )
        else:  # text-bison por defecto
            content = await service.generate_text_with_bison(
                prompt=request.prompt,
                temperature=request.temperature,
                max_output_tokens=request.max_output_tokens,
                top_p=request.top_p,
                top_k=request.top_k
            )
        
        return {
            "content": content,
            "model_used": request.model,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando texto: {str(e)}"
        )
