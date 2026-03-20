#utiliza la librería requests para realizar peticiones,comunicamos con la api
import requests
from app.config.settings import Settings

class TMDBClient:
    def __init__(self):
        self.api_key = Settings.TMDB_API_KEY
        self.base_url = Settings.TMDB_BASE_URL
        self.language = Settings.LANGUAGE

    def get(self, endpoint, params=None):
        if not self.api_key:
            raise ValueError("No se encontró la API Key. Revisa el archivo .env")

        if params is None:
            params = {}

        params["api_key"] = self.api_key
        params["language"] = self.language

        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()