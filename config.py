# config.py
# Configuration file for API keys, endpoints, and processing parameters.

# SerpAPI configuration
SERPAPI_KEY = "..."
SERPAPI_SEARCH_URL = "https://serpapi.com/search"

# Video processing configuration
FRAME_INTERVAL_SECONDS = 2  # Extract one frame every 2 seconds

# OpenAI configuration for vision analysis
OPENAI_API_KEY = "..."
OPENAI_MODEL = "gpt-4o-mini"  # Adjust to your current model

# Other configurations
OUTPUT_DIR = "./output"  # Directory to store extracted frames
IMAGE_FOLDER = "./roomPics"  # Folder containing images for OpenAI analysis
