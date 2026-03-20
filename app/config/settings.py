import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
    TMDB_IMAGE_URL = os.getenv("TMDB_IMAGE_URL", "https://image.tmdb.org/t/p/w500")
    LANGUAGE = "es-ES"