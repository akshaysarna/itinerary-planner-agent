"""
Validation Module for Itinerary Planner Agent

This module provides input validation functions for user-supplied data.
All validators follow a consistent pattern: return bool instead of raising exceptions.

Usage:
    from validation import valid_city
    
    if not valid_city("New York"):
        raise ValueError("Invalid city name")

Future expansion:
    - valid_email() for booking confirmations
    - valid_date_range() for trip dates
    - valid_phone_number() for contact information
"""

import re
import logging

# Regex patterns - Centralized for easy maintenance
PATTERNS = {
    'city': r"^[a-zA-Z\s\-\',.&()àáâãäåèéêëìíîïòóôõöùúûüñçÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÑÇ]{2,100}$",
}

# Error messages - Centralized for consistency
ERROR_MESSAGES = {
    'city': "City must be 2-100 characters with letters, spaces, hyphens, or apostrophes."
}

# Configuration constants
CITY_MIN_LENGTH = 2
CITY_MAX_LENGTH = 100


def valid_city(city: str) -> bool:
    """
    Validates city/location name format for travel planning.
    
    Validates that city name conforms to:
    - Type: Must be a string
    - Length: 2-100 characters
    - Characters: Letters, spaces, hyphens, apostrophes, commas, periods, parentheses
    - Format: No control characters, no numerics, no special symbols
    - Examples: "New York", "São Paulo", "Saint-Petersburg", "O'Fallon", "Los Angeles"
    
    Args:
        city (str): City name to validate (e.g., "Delhi", "New York")
        
    Returns:
        bool: True if city name is valid format, False otherwise
        
    Examples:
        >>> valid_city("New York")
        True
        >>> valid_city("São Paulo")
        True
        >>> valid_city("Saint-Petersburg")
        True
        >>> valid_city("New\\nYork")  # Newline
        False
        >>> valid_city("City123")  # Numbers
        False
        >>> valid_city("")
        False
        >>> valid_city(123)  # Not a string
        False
    """
    
    # LAYER 1: Type checking
    if not isinstance(city, str):
        logging.warning(f"City validation failed: Expected str, got {type(city).__name__}")
        return False
    
    # LAYER 2: Strip and normalize whitespace
    city = city.strip()
    city = " ".join(city.split())  # Remove extra spaces, normalize tabs/newlines
    
    # LAYER 3: Length validation (DoS prevention)
    if not city or len(city) < CITY_MIN_LENGTH or len(city) > CITY_MAX_LENGTH:
        logging.debug(f"City validation failed: Length {len(city)} not in range [{CITY_MIN_LENGTH}, {CITY_MAX_LENGTH}]")
        return False
    
    # LAYER 4: Pattern validation (Injection prevention)
    if not re.match(PATTERNS['city'], city):
        logging.debug(f"City validation failed: Invalid characters in '{city}'")
        return False
    
    return True
