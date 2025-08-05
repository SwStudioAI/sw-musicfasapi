"""
Servicio de integración con Google Vertex AI
"""

from typing import AsyncGenerator, List, Optional
import base64
import logging
import os
from google import genai
from google.genai import types
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError

from app.core.config import settings

logger = logging.getLogger(__name__)


class VertexAIService:
    """Servicio para interactuar con Google Vertex AI"""
    
    def __init__(self):
        """Inicializa el cliente de Vertex AI"""
        self.client = None
        self.model = settings.VERTEX_AI_MODEL
        self.is_initialized = False
        self._initialize_client()

    def _initialize_client(self):
        """Inicializa el cliente de Vertex AI con manejo de errores mejorado"""
        try:
            # Verificar que las variables de entorno necesarias estén configuradas
            if not settings.GOOGLE_CLOUD_PROJECT:
                logger.warning("GOOGLE_CLOUD_PROJECT no está configurado")
                return
            
            # Verificar credenciales
            try:
                credentials, project = default()
                logger.info(f"Credenciales encontradas para proyecto: {project}")
            except DefaultCredentialsError:
                logger.warning(
                    "No se encontraron credenciales de Google Cloud. "
                    "Configura las credenciales usando 'gcloud auth application-default login' "
                    "o establece la variable de entorno GOOGLE_APPLICATION_CREDENTIALS"
                )
                return

            # Inicializar cliente
            self.client = genai.Client(
                vertexai=True,
                project=settings.GOOGLE_CLOUD_PROJECT,
                location=settings.GOOGLE_CLOUD_LOCATION,
            )
            
            self.is_initialized = True
            logger.info(f"Vertex AI inicializado con proyecto: {settings.GOOGLE_CLOUD_PROJECT}")
            
        except Exception as e:
            logger.error(f"Error inicializando Vertex AI: {e}")
            self.client = None
            self.is_initialized = False

    def _check_client(self):
        """Verifica que el cliente esté inicializado"""
        if not self.is_initialized or self.client is None:
            raise Exception(
                "Vertex AI no está inicializado correctamente. "
                "Verifica la configuración de Google Cloud y las credenciales."
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
        """
        Genera contenido de forma streaming
        
        Args:
            prompt: El texto de entrada para generar contenido
            temperature: Controla la aleatoriedad de la respuesta
            top_p: Controla la diversidad de la respuesta
            max_output_tokens: Máximo número de tokens en la respuesta
            
        Yields:
            str: Fragmentos de texto generado
        """
        self._check_client()
        
        try:
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=prompt)
                    ]
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
        """
        Genera contenido de forma síncrona
        
        Args:
            prompt: El texto de entrada para generar contenido
            temperature: Controla la aleatoriedad de la respuesta
            top_p: Controla la diversidad de la respuesta
            max_output_tokens: Máximo número de tokens en la respuesta
            
        Returns:
            str: El contenido generado completo
        """
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

    async def generate_music_analysis(self, audio_data: bytes) -> str:
        """
        Analiza datos de audio usando Vertex AI
        
        Args:
            audio_data: Datos de audio en bytes
            
        Returns:
            str: Análisis del audio generado por IA
        """
        self._check_client()
        
        try:
            # Codificar audio en base64 para envío
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text="Analiza este archivo de audio y proporciona información sobre género musical, tempo, instrumentos detectados y características generales:"),
                        types.Part(
                            inline_data=types.Blob(
                                mime_type="audio/wav",  # Ajustar según el tipo de audio
                                data=audio_base64
                            )
                        )
                    ]
                )
            ]

            config = self._create_generate_config(temperature=0.3)  # Menos creatividad para análisis

            result = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=config,
            ):
                if chunk.text:
                    result += chunk.text

            return result

        except Exception as e:
            logger.error(f"Error analyzing music: {e}")
            raise

    async def generate_music_recommendation(
        self,
        user_preferences: dict,
        listening_history: List[dict]
    ) -> str:
        """
        Genera recomendaciones musicales personalizadas
        
        Args:
            user_preferences: Preferencias del usuario
            listening_history: Historial de reproducción
            
        Returns:
            str: Recomendaciones musicales generadas
        """
        try:
            prompt = f"""
            Basándote en las siguientes preferencias del usuario y su historial de reproducción,
            genera recomendaciones musicales personalizadas:

            Preferencias del usuario:
            {user_preferences}

            Historial de reproducción reciente:
            {listening_history}

            Por favor, proporciona:
            1. 5 canciones recomendadas con artista y título
            2. Géneros musicales que podrían interesar al usuario
            3. Breve explicación de por qué estas recomendaciones encajan con sus gustos
            """

            return await self.generate_content(
                prompt=prompt,
                temperature=0.7,  # Creatividad moderada para recomendaciones
                max_output_tokens=2048
            )

        except Exception as e:
            logger.error(f"Error generating music recommendations: {e}")
            raise


# Instancia global del servicio (se inicializa de forma lazy)
vertex_ai_service = None

def get_vertex_ai_service() -> VertexAIService:
    """Obtiene la instancia del servicio Vertex AI (patrón singleton lazy)"""
    global vertex_ai_service
    if vertex_ai_service is None:
        vertex_ai_service = VertexAIService()
    return vertex_ai_service
