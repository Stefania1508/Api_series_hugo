from app.infrastructure.tmdb_client import TMDBClient

class SeriesRepository:
    def __init__(self):
        self.client = TMDBClient()

    def search_series(self, query):
        return self.client.get("/search/tv", {"query": query})

    def get_series_details(self, series_id):
        return self.client.get(f"/tv/{series_id}")

    def get_series_credits(self, series_id):
        return self.client.get(f"/tv/{series_id}/credits")

    def get_series_videos(self, series_id):
        return self.client.get(f"/tv/{series_id}/videos")

    def get_series_recommendations(self, series_id):
        return self.client.get(f"/tv/{series_id}/recommendations")

    def get_series_similar(self, series_id):
        return self.client.get(f"/tv/{series_id}/similar")

    def get_season_details(self, series_id, season_number):
        return self.client.get(f"/tv/{series_id}/season/{season_number}")
    
    