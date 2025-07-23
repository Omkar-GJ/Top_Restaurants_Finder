
import requests
import json

def get_top_restaurants(city, api_key):
    # create query
    query = f"top restaurants in {city}"
    
    # API endpoint and parameters
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "location": city,
        "hl": "en",
        "gl": "us",
        "api_key": api_key,
        "engine": "google_maps"
    }

    # call SerpAPI
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("Failed to fetch data.")
        return {}

    data = response.json()
    
    # Get restaurant information
    restaurants = {}
    try:
        local_results = data.get("local_results", {}).get("places", [])
        
        for place in local_results[:10]:  
	    # Top 10 only
            name = place.get("title", "Unknown")
            rating = place.get("rating", "No rating")
            reviews = place.get("reviews", "No reviews")
            address = place.get("address", "No address")

            restaurants[name] = {
                "rating": rating,
                "reviews": reviews,
                "address": address
            }

    except Exception as e:
        print("Error parsing data:", e)

    return restaurants

def main():
    print("Top 10 Restaurants Finder")
    city = input("Enter city name: ").strip()
    api_key = input("Enter your SerpAPI Key: ").strip()

    print(f"\nSearching top restaurants in {city}...\n")
    top_restaurants = get_top_restaurants(city, api_key)

    if top_restaurants:
        # Save to JSON
        filename = f"{city.replace(' ', '_').lower()}_top_restaurants.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(top_restaurants, f, indent=4)
        print(f"\nTop restaurants saved to '{filename}'")
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
