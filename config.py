from dataclasses import dataclass, field

@dataclass
class APIConfig:
    GOOGLE_MAPS_API_TIMEOUT: int = field(default=10)
    GOOGLE_MAPS_RETRY_ATTEMPTS: int = field(default=2)
    SEARCH_API_TIMEOUT: int = field(default=5)
    SEARCH_API_RETRY_ATTEMPTS: int = field(default=2)
    AIRPORT_MAX_RESULTS: int = field(default=2)
    HOTEL_MAX_RESULTS: int = field(default=5)
    HOTEL_MIN_RATING: float = field(default=3.5)

    def __post_init__(self):
        if self.GOOGLE_MAPS_API_TIMEOUT <= 0:
            raise ValueError("GOOGLE_MAPS_API_TIMEOUT must be a positive integer.")
        if self.GOOGLE_MAPS_RETRY_ATTEMPTS < 0:
            raise ValueError("GOOGLE_MAPS_RETRY_ATTEMPTS cannot be negative.")
        if self.SEARCH_API_TIMEOUT <= 0:
            raise ValueError("SEARCH_API_TIMEOUT must be a positive integer.")
        if self.SEARCH_API_RETRY_ATTEMPTS < 0:
            raise ValueError("SEARCH_API_RETRY_ATTEMPTS cannot be negative.")
        if self.AIRPORT_MAX_RESULTS <= 0:
            raise ValueError("AIRPORT_MAX_RESULTS must be a positive integer.")
        if self.HOTEL_MAX_RESULTS <= 0:
            raise ValueError("HOTEL_MAX_RESULTS must be a positive integer.")
        if not (0.0 <= self.HOTEL_MIN_RATING <= 5.0):
            raise ValueError("HOTEL_MIN_RATING must be between 0.0 and 5.0.")

API_CONFIG = APIConfig()