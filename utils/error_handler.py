"""
Error handling utilities for the Fingrid data application.
"""


class FingridAPIError(Exception):
    """Base exception for Fingrid API errors."""
    pass


class AuthenticationError(FingridAPIError):
    """Raised when API authentication fails."""
    pass


class NetworkError(FingridAPIError):
    """Raised when network connectivity fails."""
    pass


class ValidationError(FingridAPIError):
    """Raised when input validation fails."""
    pass


class DataProcessingError(FingridAPIError):
    """Raised when data processing fails."""
    pass


def handle_error(e):
    """
    Handle and display errors appropriately.
    
    Args:
        e (Exception): The exception to handle.
    """
    error_messages = {
        AuthenticationError: "Authentication failed. Please check your API key.",
        NetworkError: "Network error. Please check your internet connection.",
        ValidationError: "Invalid input. Please check the provided parameters.",
        DataProcessingError: "Error processing data. Please try again.",
        ValueError: "Invalid value provided. Please check your input.",
        ConnectionError: "Failed to connect to the API. Please try again later.",
    }
    
    error_type = type(e)
    message = error_messages.get(error_type, str(e))
    
    print(f"\n❌ Error: {message}")
    if str(e) and str(e) != message:
        print(f"   Details: {str(e)}")


def validate_time_format(time_str):
    """
    Validate ISO 8601 time format (YYYY-MM-DDTHH:MM:SSZ or similar).
    
    Args:
        time_str (str): The time string to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    from datetime import datetime
    try:
        # Try multiple ISO formats
        for fmt in ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
            try:
                datetime.strptime(time_str, fmt)
                return True
            except ValueError:
                continue
        return False
    except Exception:
        return False
