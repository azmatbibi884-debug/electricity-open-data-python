import os

API_KEY = os.getenv("FINGRID_API_KEY")
BASE_URL = "https://api.fingrid.fi/v1/variable"

# Note: API_KEY is optional. It's only required when using the live API client.
# Demo mode and example scripts work without it.
