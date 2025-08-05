"""
Servicio de integración con Google Cloud AI Platform
Usando las bibliotecas oficiales vertexai y google-cloud-aiplatform
"""

from typing import List, Optional, Dict, Any
import logging
import os
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextGenerationModel
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError

from app.core.config import settings

logger = logging.getLogger(__name__)


class GoogleCloudAIService:
    """Servicio para interactuar con Google Cloud AI Platform"""
    
    def __init__(self):
        """Inicializa el servicio de Google Cloud AI"""
        self.is_initialized = False
        self.project_id = settings.GOOGLE_CLOUD_PROJECT
        self.location = settings.GOOGLE_CLOUD_LOCATION
        self._initialize_client()

    def _initialize_client(self):
        """Inicializa el cliente de Google Cloud AI Platform"""
        try:
            # Verificar que el proyecto esté configurado
            if not self.project_id:
                logger.warning("GOOGLE_CLOUD_PROJECT no está configurado")
                return
            
            # Verificar credenciales
            try:
                credentials, project = default()
                logger.info(f"Credenciales encontradas para proyecto: {project}")
            except DefaultCredentialsError:
                logger.warning(
                    "No se encontraron credenciales de Google Cloud. "
                    "Configura las credenciales usando 'gcloud auth application-default login'"
                )
                return

            # Inicializar Vertex AI
            vertexai.init(
                project=self.project_id,
                location=self.location
            )
            
            self.is_initialized = True
            logger.info(f"Google Cloud AI Platform inicializado - Proyecto: {self.project_id}, Región: {self.location}")
            
        except Exception as e:
            logger.error(f"Error inicializando Google Cloud AI Platform: {e}")
            self.is_initialized = False

    def _check_initialization(self):
        """Verifica que el servicio esté inicializado"""
        if not self.is_initialized:
            raise Exception(
                "Google Cloud AI Platform no está inicializado. "
                "Verifica la configuración del proyecto y las credenciales."
            )

    async def generate_text_with_bison(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
        top_p: float = 0.8,
        top_k: int = 40
    ) -> str:
        """
        Genera texto usando el modelo text-bison
        
        Args:
            prompt: El texto de entrada
            temperature: Controla la aleatoriedad (0.0 - 1.0)
            max_output_tokens: Máximo número de tokens en la respuesta
            top_p: Controla la diversidad de la respuesta
            top_k: Limita las opciones de tokens
            
        Returns:
            str: El texto generado
        """
        self._check_initialization()
        
        try:
            # Cargar el modelo text-bison
            model = TextGenerationModel.from_pretrained("text-bison")
            
            # Realizar la predicción
            response = model.predict(
                prompt=prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k
            )
            
            logger.info(f"Texto generado exitosamente para prompt: {prompt[:50]}...")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generando texto con text-bison: {e}")
            raise

    async def generate_text_with_gemini(
        self,
        prompt: str,
        temperature: float = 0.9,
        max_output_tokens: int = 2048,
        top_p: float = 1.0,
        top_k: int = 32
    ) -> str:
        """
        Genera texto usando el modelo Gemini Pro
        
        Args:
            prompt: El texto de entrada
            temperature: Controla la aleatoriedad
            max_output_tokens: Máximo número de tokens
            top_p: Controla la diversidad
            top_k: Limita las opciones de tokens
            
        Returns:
            str: El texto generado
        """
        self._check_initialization()
        
        try:
            # Cargar el modelo Gemini Pro
            model = GenerativeModel("gemini-pro")
            
            # Configurar parámetros de generación
            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
            }
            
            # Generar contenido
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            logger.info(f"Texto generado con Gemini para prompt: {prompt[:50]}...")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generando texto con Gemini: {e}")
            raise

    async def generate_music_intro(
        self,
        style: str = "radio",
        genre: str = "pop",
        language: str = "español",
        duration: str = "30 segundos"
    ) -> str:
        """
        Genera un intro musical personalizado
        
        Args:
            style: Estilo del intro (radio, podcast, show, etc.)
            genre: Género musical
            language: Idioma del intro
            duration: Duración aproximada
            
        Returns:
            str: El intro generado
        """
        prompt = f"""
        Genera un intro de {style} en {language} para un programa de música {genre}.
        El intro debe:
        - Durar aproximadamente {duration}
        - Ser energético y atractivo
        - Incluir una llamada a la acción
        - Mencionar el género musical {genre}
        - Tener un tono profesional pero amigable
        
        Ejemplo de formato:
        "¡Bienvenidos a [Nombre del programa]! Tu destino para la mejor música {genre}..."
        """
        
        try:
            return await self.generate_text_with_bison(
                prompt=prompt,
                temperature=0.8,
                max_output_tokens=512
            )
        except Exception:
            # Fallback a Gemini si text-bison falla
            return await self.generate_text_with_gemini(
                prompt=prompt,
                temperature=0.8,
                max_output_tokens=512
            )

    async def analyze_music_preferences(
        self,
        user_data: Dict[str, Any]
    ) -> str:
        """
        Analiza las preferencias musicales del usuario
        
        Args:
            user_data: Datos del usuario (historial, géneros favoritos, etc.)
            
        Returns:
            str: Análisis de preferencias
        """
        prompt = f"""
        Analiza las siguientes preferencias musicales del usuario y proporciona insights:
        
        Datos del usuario:
        {user_data}
        
        Proporciona:
        1. Resumen de géneros favoritos
        2. Patrones de escucha
        3. Recomendaciones de nuevos géneros
        4. Artistas similares que podrían gustar
        5. Tendencias musicales relevantes
        """
        
        return await self.generate_text_with_gemini(
            prompt=prompt,
            temperature=0.6,
            max_output_tokens=1024
        )

    async def generate_playlist_description(
        self,
        playlist_name: str,
        songs: List[str],
        theme: str = ""
    ) -> str:
        """
        Genera una descripción para una playlist
        
        Args:
            playlist_name: Nombre de la playlist
            songs: Lista de canciones
            theme: Tema o mood de la playlist
            
        Returns:
            str: Descripción generada
        """
        songs_text = "\n".join(songs[:10])  # Limitar a 10 canciones
        
        prompt = f"""
        Genera una descripción atractiva para una playlist llamada "{playlist_name}".
        
        Tema/Mood: {theme}
        
        Canciones incluidas:
        {songs_text}
        
        La descripción debe:
        - Capturar el mood/atmósfera de las canciones
        - Ser atractiva para los usuarios
        - Mencionar cuándo es ideal escuchar esta playlist
        - Tener entre 50-150 palabras
        """
        
        return await self.generate_text_with_bison(
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=256
        )

    async def get_service_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado del servicio
        
        Returns:
            Dict con información del estado
        """
        return {
            "initialized": self.is_initialized,
            "project_id": self.project_id,
            "location": self.location,
            "available_models": [
                "text-bison",
                "gemini-pro"
            ]
        }

    async def test_connection(self) -> str:
        """
        Prueba la conexión con un prompt simple
        
        Returns:
            str: Respuesta de prueba
        """
        test_prompt = "Escribe un saludo corto y amigable para probar la conexión."
        
        try:
            return await self.generate_text_with_bison(
                prompt=test_prompt,
                temperature=0.5,
                max_output_tokens=100
            )
        except Exception:
            # Fallback a Gemini
            return await self.generate_text_with_gemini(
                prompt=test_prompt,
                temperature=0.5,
                max_output_tokens=100
            )


# Instancia global del servicio
google_ai_service = None

def get_google_ai_service() -> GoogleCloudAIService:
    """Obtiene la instancia del servicio Google Cloud AI"""
    global google_ai_service
    if google_ai_service is None:
        google_ai_service = GoogleCloudAIService()
    return google_ai_service
