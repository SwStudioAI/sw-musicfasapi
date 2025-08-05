"""
Versión simplificada del servicio Vertex AI usando API Key
Para usar cuando no tienes Google Cloud CLI configurado
"""

from typing import AsyncGenerator, List, Optional
import base64
import logging
import os
import httpx
from google import genai
from google.genai import types

from app.core.config import settings

logger = logging.getLogger(__name__)


class VertexAIServiceSimple:
    """Servicio simplificado para Vertex AI usando API Key"""
    
    def __init__(self):
        """Inicializa el cliente con API Key"""
        self.client = None
        self.model = settings.VERTEX_AI_MODEL
        self.is_initialized = False
        self._initialize_client()

    def _initialize_client(self):
        """Inicializa el cliente usando API Key"""
        try:
            # Verificar si hay API Key configurada
            if settings.GOOGLE_API_KEY:
                logger.info("Inicializando con Google API Key")
                self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
                self.is_initialized = True
                logger.info("Vertex AI inicializado con API Key")
                return
            
            # Si no hay API Key, intentar con credenciales por defecto
            if settings.GOOGLE_CLOUD_PROJECT:
                logger.info("Intentando inicializar con credenciales por defecto")
                try:
                    from google.auth import default
                    credentials, project = default()
                    
                    self.client = genai.Client(
                        vertexai=True,
                        project=settings.GOOGLE_CLOUD_PROJECT,
                        location=settings.GOOGLE_CLOUD_LOCATION,
                    )
                    self.is_initialized = True
                    logger.info(f"Vertex AI inicializado con proyecto: {settings.GOOGLE_CLOUD_PROJECT}")
                except Exception as e:
                    logger.warning(f"No se pudo inicializar con credenciales por defecto: {e}")
            
            if not self.is_initialized:
                logger.error(
                    "No se pudo inicializar Vertex AI. "
                    "Configura GOOGLE_API_KEY o credenciales de Google Cloud."
                )
                
        except Exception as e:
            logger.error(f"Error inicializando Vertex AI: {e}")
            self.client = None
            self.is_initialized = False

    def _check_client(self):
        """Verifica que el cliente esté inicializado"""
        if not self.is_initialized or self.client is None:
            raise Exception(
                "Vertex AI no está inicializado. "
                "Configura GOOGLE_API_KEY o credenciales de Google Cloud."
            )

    def _create_safety_settings(self) -> List[types.SafetySetting]:
        """Crea la configuración de seguridad para el modelo"""
        return [
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ]

    def _create_generate_config(
        self,
        temperature: float = 1.0,
        top_p: float = 0.95,
        max_output_tokens: int = 65535
    ) -> types.GenerateContentConfig:
        """Crea la configuración de generación de contenido"""
        return types.GenerateContentConfig(
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_output_tokens,
            safety_settings=self._create_safety_settings(),
            thinking_config=types.ThinkingConfig(
                thinking_budget=-1,
            ),
        )

    async def generate_content_stream(
        self,
        prompt: str,
        temperature: float = 1.0,
        top_p: float = 0.95,
        max_output_tokens: int = 65535
    ) -> AsyncGenerator[str, None]:
        """Genera contenido de forma streaming"""
        self._check_client()
        
        try:
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part(text=prompt)]
                )
            ]

            config = self._create_generate_config(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_output_tokens
            )

            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=config,
            ):
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Error generating content stream: {e}")
            raise

    async def generate_content(
        self,
        prompt: str,
        temperature: float = 1.0,
        top_p: float = 0.95,
        max_output_tokens: int = 65535
    ) -> str:
        """Genera contenido de forma síncrona"""
        try:
            result = ""
            async for chunk in self.generate_content_stream(
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_output_tokens
            ):
                result += chunk
            return result

        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise

    async def get_status(self) -> dict:
        """Obtiene el estado del servicio"""
        return {
            "initialized": self.is_initialized,
            "model": self.model,
            "auth_method": "API_KEY" if settings.GOOGLE_API_KEY else "DEFAULT_CREDENTIALS",
            "project": settings.GOOGLE_CLOUD_PROJECT or "No configurado"
        }


# Instancia global del servicio simplificado
vertex_ai_service_simple = None

def get_vertex_ai_service_simple() -> VertexAIServiceSimple:
    """Obtiene la instancia del servicio Vertex AI simplificado"""
    global vertex_ai_service_simple
    if vertex_ai_service_simple is None:
        vertex_ai_service_simple = VertexAIServiceSimple()
    return vertex_ai_service_simple
