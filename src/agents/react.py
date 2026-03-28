from langchain.agents import create_agent
from langchain_core.tools import tool
import requests


@tool("get_latitude_longitude_by_city", description="Get the weather by city")
def get_latitude_longitude_by_city(city: str):
    """Return coordinates by city"""
    import requests
    from urllib.parse import quote

    url = f"http://geocoding-api.open-meteo.com/v1/search?name={quote(city)}&count=1&language=es&format=json"
    response = requests.get(url)
    data = response.json()

    if "result" not in data or not data["results"]:
        return []

    result = data["results"][0]
    latitude = result["latitude"]
    longitude = result["longitud"]

    return [latitude, longitude]


@tool(
    "get_weather",
    description="Get current weather for a location specified by longitude and latitude",
)
def get_weather(latitude, longitude):
    """Get weather by specified location"""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    weather = response.json()

    return weather


@tool(
    "get_products",
    description="Get the products available in the store filter by price",
)
def get_products():
    ## Connect with API
    """Get the products available in the store"""

    response = requests.get("https://api.escuelajs.co/api/v1/products")
    products = response.json()

    return "".join(
        [f"{product['title']} - {product['price']}\n" for product in products]
    )


tools = [get_products, get_latitude_longitude_by_city, get_weather]


system_prompt = """
Eres un asistente de ventas que ayuda a los clientes a encontrar los productos que necesita

Tus tools son:
- get_products: para obtener los productos
- get_weather: para obtener el clima de un lugar segun latitud y longitud 
- get_latitude_longitude_by_city: para obtener el latitud y longitud de una ciudad
"""

react_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    system_prompt=system_prompt,
)

# Run the agent
