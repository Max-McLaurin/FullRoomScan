# price_estimator.py
import requests
from config import SERPAPI_KEY, SERPAPI_SEARCH_URL

def query_serpapi(asset_description):
    """
    Query SerpAPI with a product description to get a price estimate.
    
    Args:
        asset_description (str): The asset description used for search.
        
    Returns:
        dict: Contains price, currency, and a simple confidence score.
    """
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "amazon",
        "q": asset_description,
        "location": "United States",
        "hl": "en"
    }
    
    response = requests.get(SERPAPI_SEARCH_URL, params=params)
    data = response.json()
    
    # Use the first result's price information if available.
    if "shopping_results" in data and data["shopping_results"]:
        result = data["shopping_results"][0]
        price = result.get("price", {}).get("raw", None)
        currency = result.get("price", {}).get("currency", "USD")
        confidence = "High"  # In production, you might calculate this based on multiple factors.
        return {
            "estimated_price": price,
            "currency": currency,
            "confidence": confidence,
            "source": "SerpAPI"
        }
    else:
        return {
            "estimated_price": None,
            "currency": None,
            "confidence": "Low",
            "source": "SerpAPI"
        }

def estimate_prices(assets):
    """
    Given a list of assets, query SerpAPI for each asset's price.
    
    Args:
        assets (list[dict]): Each dict contains asset details (name, description).
    
    Returns:
        list[dict]: List of assets enriched with price estimates.
    """
    priced_assets = []
    for asset in assets:
        price_info = query_serpapi(asset["description"])
        asset_with_price = asset.copy()
        asset_with_price.update(price_info)
        priced_assets.append(asset_with_price)
    return priced_assets

if __name__ == "__main__":
    # Test the price estimator with a sample asset.
    sample_asset = {"name": "Lamp", "description": "Modern Black Desk Lamp with Adjustable Arm"}
    result = query_serpapi(sample_asset["description"])
    print("Price estimate result:", result)
