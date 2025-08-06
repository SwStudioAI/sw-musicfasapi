from fastapi import APIRouter, HTTPException, Request, Depends, Query, Header
from pydantic import BaseModel
from typing import Optional, List
import httpx
import logging
from app.core.config import settings
from app.api.deps import CurrentUser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/soundcloud", tags=["soundcloud"])


class SoundCloudTokenRequest(BaseModel):
    """Modelo para solicitar token de SoundCloud"""
    code: str


class SoundCloudTokenResponse(BaseModel):
    """Respuesta del token de SoundCloud"""
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    token_type: Optional[str] = None
    success: bool = True
    error: Optional[str] = None


class SoundCloudTrack(BaseModel):
    """Modelo para una canción de SoundCloud"""
    id: int
    title: str
    duration_minutes: float
    duration_ms: int
    permalink_url: Optional[str] = None
    embed_url: Optional[str] = None
    artwork_url: Optional[str] = None
    user_name: Optional[str] = None
    genre: Optional[str] = None
    created_at: Optional[str] = None


class SoundCloudTracksResponse(BaseModel):
    """Respuesta con lista de canciones de SoundCloud"""
    tracks: List[SoundCloudTrack]
    total_count: int
    success: bool = True
    error: Optional[str] = None


@router.post("/auth/token", response_model=SoundCloudTokenResponse)
async def get_soundcloud_token(request: SoundCloudTokenRequest):
    """
    Intercambia el código de autorización por un access_token de SoundCloud
    """
    try:
        url = "https://api.soundcloud.com/oauth2/token"
        
        data = {
            "client_id": settings.SOUNDCLOUD_CLIENT_ID,
            "client_secret": settings.SOUNDCLOUD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": settings.SOUNDCLOUD_REDIRECT_URI,
            "code": request.code,
        }
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, data=data, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"SoundCloud token error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error obteniendo token de SoundCloud: {response.text}"
                )
            
            result = response.json()
            
            return SoundCloudTokenResponse(
                access_token=result.get("access_token", ""),
                refresh_token=result.get("refresh_token"),
                expires_in=result.get("expires_in"),
                scope=result.get("scope"),
                token_type=result.get("token_type"),
                success=True
            )
            
    except httpx.RequestError as e:
        logger.error(f"Network error requesting SoundCloud token: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error de conexión con SoundCloud"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting SoundCloud token: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@router.get("/tracks", response_model=SoundCloudTracksResponse)
async def get_soundcloud_tracks(
    current_user: CurrentUser,
    access_token: Optional[str] = Query(None, description="SoundCloud access token"),
    authorization: Optional[str] = Header(None, description="Authorization header with Bearer token")
):
    """
    Obtiene las canciones del usuario autenticado de SoundCloud
    """
    try:
        # Extraer token del header Authorization o del query parameter
        token = access_token
        if not token and authorization:
            if authorization.startswith("Bearer "):
                token = authorization.replace("Bearer ", "")
            elif authorization.startswith("OAuth "):
                token = authorization.replace("OAuth ", "")
            else:
                token = authorization
        
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Access token de SoundCloud requerido (query param 'access_token' o header 'Authorization')"
            )
        
        url = "https://api.soundcloud.com/me/tracks"
        headers = {"Authorization": f"OAuth {token}"}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Token de SoundCloud inválido o expirado"
                )
            elif response.status_code != 200:
                logger.error(f"SoundCloud tracks error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error obteniendo canciones de SoundCloud: {response.text}"
                )
            
            tracks_raw = response.json()
            
            # Procesar tracks
            tracks = []
            for track_data in tracks_raw:
                # Calcular duración en minutos
                duration_ms = track_data.get("duration", 0)
                duration_minutes = round(duration_ms / 60000, 2) if duration_ms else 0
                
                # Generar URL de embed
                embed_url = None
                if track_data.get("permalink_url"):
                    embed_url = f"https://w.soundcloud.com/player/?url={track_data['permalink_url']}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"
                
                track = SoundCloudTrack(
                    id=track_data.get("id", 0),
                    title=track_data.get("title", "Sin título"),
                    duration_minutes=duration_minutes,
                    duration_ms=duration_ms,
                    permalink_url=track_data.get("permalink_url"),
                    embed_url=embed_url,
                    artwork_url=track_data.get("artwork_url"),
                    user_name=track_data.get("user", {}).get("username") if track_data.get("user") else None,
                    genre=track_data.get("genre"),
                    created_at=track_data.get("created_at")
                )
                tracks.append(track)
            
            return SoundCloudTracksResponse(
                tracks=tracks,
                total_count=len(tracks),
                success=True
            )
            
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.error(f"Network error requesting SoundCloud tracks: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error de conexión con SoundCloud"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting SoundCloud tracks: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@router.get("/auth/url")
async def get_soundcloud_auth_url():
    """
    Devuelve la URL de autorización de SoundCloud para redirigir al usuario
    """
    auth_url = (
        f"https://soundcloud.com/connect?"
        f"client_id={settings.SOUNDCLOUD_CLIENT_ID}&"
        f"redirect_uri={settings.SOUNDCLOUD_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=non-expiring"
    )
    
    return {
        "auth_url": auth_url,
        "client_id": settings.SOUNDCLOUD_CLIENT_ID,
        "redirect_uri": settings.SOUNDCLOUD_REDIRECT_URI,
        "success": True
    }
