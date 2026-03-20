from app.repositories.series_repository import SeriesRepository
from app.config.settings import Settings


class SeriesService:
    def __init__(self):
        self.repository = SeriesRepository()
        self.image_base_url = Settings.TMDB_IMAGE_URL

    def _is_valid_query(self, query):
        if not query:
            return False

        normalized = query.strip().lower()
        valid_names = [
            "attack on titan",
            "shingeki no kyojin"
        ]
        return normalized in valid_names

    def _find_attack_on_titan(self):
        # ENDPOINT 1: /search/tv
        search_data = self.repository.search_series("Attack on Titan")
        results = search_data.get("results", [])

        if not results:
            return None

        for item in results:
            name = (item.get("name") or "").lower()
            original_name = (item.get("original_name") or "").lower()

            if "attack on titan" in name or "shingeki no kyojin" in original_name:
                return item

        return results[0] if results else None

    def search_series_data(self, query):
        if not self._is_valid_query(query):
            return {"not_allowed": True}

        selected_series = self._find_attack_on_titan()

        if not selected_series:
            return {"error": "No se encontró la serie Attack on Titan."}

        series_id = selected_series["id"]

        #ENDPOINT 2: /tv/{series_id}
        details = self.repository.get_series_details(series_id)

        # ENDPOINT 3: /tv/{series_id}/credits
        credits = self.repository.get_series_credits(series_id)

        # ENDPOINT 4: /tv/{series_id}/videos
        videos = self.repository.get_series_videos(series_id)

        # ENDPOINT 6: /tv/{series_id}/recommendations
        recommendations = self.repository.get_series_recommendations(series_id)

        trailer_url = None
        for video in videos.get("results", []):
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                trailer_url = f"https://www.youtube.com/embed/{video.get('key')}?rel=0&modestbranding=1&controls=1"
                break

        cast = credits.get("cast", [])[:10]
        seasons = details.get("seasons", [])

        seasons_data = []
        for season in seasons:
            season_number = season.get("season_number")

            if season_number is None:
                continue

            # ENDPOINT 5: /tv/{series_id}/season/{season_number}
            season_detail = self.repository.get_season_details(series_id, season_number)
            episodes = season_detail.get("episodes", [])

            seasons_data.append({
                "season_number": season_number,
                "name": season.get("name"),
                "poster": f"{self.image_base_url}{season.get('poster_path')}" if season.get("poster_path") else None,
                "episode_count": season.get("episode_count"),
                "episodes": [
                    {
                        "episode_number": ep.get("episode_number"),
                        "name": ep.get("name"),
                        "overview": ep.get("overview"),
                        "still_path": f"{self.image_base_url}{ep.get('still_path')}" if ep.get("still_path") else None,
                        "air_date": ep.get("air_date")
                    }
                    for ep in episodes
                ]
            })

        return {
            "name": details.get("name"),
            "overview": details.get("overview"),
            "poster": f"{self.image_base_url}{details.get('poster_path')}" if details.get("poster_path") else None,
            "backdrop": f"{self.image_base_url}{details.get('backdrop_path')}" if details.get("backdrop_path") else None,
            "first_air_date": details.get("first_air_date"),
            "vote_average": details.get("vote_average"),
            "number_of_seasons": details.get("number_of_seasons"),
            "number_of_episodes": details.get("number_of_episodes"),
            "genres": [genre["name"] for genre in details.get("genres", [])],
            "cast": [
                {
                    "name": actor.get("name"),
                    "character": actor.get("character"),
                    "profile_path": f"{self.image_base_url}{actor.get('profile_path')}" if actor.get("profile_path") else None
                }
                for actor in cast
            ],
            "trailer_url": trailer_url,
            "seasons": seasons_data,
            "recommendations": [
                {
                    "name": item.get("name"),
                    "poster": f"{self.image_base_url}{item.get('poster_path')}" if item.get("poster_path") else None,
                    "vote_average": item.get("vote_average")
                }
                for item in recommendations.get("results", [])[:6]
            ]
        }