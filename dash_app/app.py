# dash_app/app.py
import dash, requests
from dash import html, dcc
from weather_app import app as app_weather
from news_app import app as app_news

# Initialize the Dash application
app = dash.Dash(__name__, requests_pathname_prefix="/dashboard/")

# External API URL (replace with the actual URL)
EXTERNAL_API_URL = "https://weather1003.azurewebsites.net/info"

 
def get_external_info():
    try:
        response = requests.get(EXTERNAL_API_URL)
        return response.json()  # Convert response to JSON
    except Exception as e:
        return {"date": "N/A", "time": "N/A", "weather": {"city": "Unknown", "temperature": "N/A", "description": "N/A"}}
info = get_external_info()

# Define Dash layout with 4 example graphs
app.layout = html.Div(children=[

    html.H1(children="WeatherAPI"),
    
    html.Div(children=f"The weather Today"),
    # Display date, time, and weather info at the top of the dashboard
    html.Div([
        html.H3(f"Date: {info['date']}"),
        html.H3(f"Time: {info['time']}"),
        html.H3(f"Weather in {info['weather']['city']}: {info['weather']['temperature']} °C, {info['weather']['description']}"),
    ], style={'marginBottom': 20}),
     # Navigation Links using html.A to redirect to FastAPI routes
    html.Div([
        html.A('Home', href='/'),  # Redirect to FastAPI's home route
        " | ",
        html.A('Logout', href='/logout')  # Redirect to FastAPI's logout route
    ], style={'marginTop': 20})   
])

# Expose the Flask server to integrate with FastAPI
server = app.server