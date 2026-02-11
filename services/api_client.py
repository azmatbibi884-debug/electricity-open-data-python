"""
API client for Fingrid Open Data API.
"""
import requests
from config import API_KEY, BASE_URL
from utils.error_handler import (
    AuthenticationError,
    NetworkError,
    ValidationError,
)


class FingridAPIClient:
    """Client for interacting with Fingrid Open Data API."""
    
    # Common electricity variable IDs
    COMMON_VARIABLES = {
        "124": "Production (Hydro)",
        "100": "Production (Wind)",
        "101": "Production (Thermal)",
        "102": "Production (Solar)",
        "74": "Electricity generation",
        "172": "Load forecast",
        "191": "Reserved capacity",
        "200": "Cross-border flow",
    }
    
    def __init__(self):
        """Initialize the API client."""
        if not API_KEY:
            raise AuthenticationError(
                "FINGRID_API_KEY is missing. Set it as an environment variable.\n"
                "Example: $env:FINGRID_API_KEY = 'your_key_here'"
            )
        self.api_key = API_KEY
        self.base_url = BASE_URL
    
    def fetch_data(self, variable_id, start_time, end_time):
        """
        Fetch data from Fingrid API.
        
        Args:
            variable_id (str): The variable ID to fetch.
            start_time (str): Start time in ISO format (e.g., 2024-01-01T00:00:00Z).
            end_time (str): End time in ISO format.
            
        Returns:
            list: Raw data from API.
            
        Raises:
            ValidationError: If parameters are invalid.
            AuthenticationError: If API key is invalid.
            NetworkError: If network request fails.
        """
        # Validate inputs
        if not variable_id:
            raise ValidationError("Variable ID cannot be empty.")
        if not start_time or not end_time:
            raise ValidationError("Start and end times are required.")
        
        url = f"{self.base_url}/{variable_id}/events/json"
        headers = {"x-api-key": self.api_key}
        params = {"start_time": start_time, "end_time": end_time}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key. Please check your FINGRID_API_KEY.")
            elif response.status_code == 404:
                raise ValidationError(f"Variable ID {variable_id} not found.")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Failed to connect to Fingrid API. Check your internet connection.")
        except requests.exceptions.HTTPError as e:
            raise NetworkError(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Error fetching data: {e}")
    
    @classmethod
    def get_common_variables(cls):
        """
        Get a dictionary of common electricity variables and their descriptions.
        
        Returns:
            dict: Variable ID -> description mapping.
        """
        return cls.COMMON_VARIABLES
