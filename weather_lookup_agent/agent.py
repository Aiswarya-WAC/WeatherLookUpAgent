import os
import requests
from google.adk.agents import Agent

# Define the weather lookup tool with a real API
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.
    
    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").
    
    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---")  # Log tool execution
    
    # Get API key from environment variable
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return {"status": "error", "error_message": "Weather API key not configured."}
    
    # Call the OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        data = response.json()
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        report = f"The weather in {city} is {weather_description} with a temperature of {temp}°C. "
        report += f"Humidity: {humidity}%, Wind speed: {wind_speed} m/s."
        
        return {"status": "success", "report": report}
        
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Error fetching weather data: {str(e)}"}
    except (KeyError, IndexError, ValueError) as e:
        return {"status": "error", "error_message": f"Error parsing weather data: {str(e)}"}

# Define the agent
weather_agent = Agent(
    name="weather_agent_v1",
    model="gemini-2.0-flash",  # Use the Gemini 2.0 Flash model
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather],
)

# Export the agent to be discovered by ADK
root_agent = weather_agent
