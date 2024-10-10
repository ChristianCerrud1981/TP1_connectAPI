# dash_app/app.py
import dash, requests
from dash import html, dcc

# Initialize the Dash application
app = dash.Dash(__name__, requests_pathname_prefix="/dashboard/")

# External API URL (replace with the actual URL)
EXTERNAL_API_URL_WEATHER = "http://127.0.0.1:8025/info"
EXTERNAL_API_URL_NEWS = "http://127.0.0.1:8015/info"

 
def get_weather_info():
    try:
        response = requests.get(EXTERNAL_API_URL_WEATHER)
        return response.json()  # Convert response to JSON
    except Exception as e:
        return {"date": "N/A", "time": "N/A", "weather": {"city": "Unknown", "temperature": "N/A", "description": "N/A"}}
infoWeather = get_weather_info()

def get_news_info():
    try:
        response = requests.get(EXTERNAL_API_URL_NEWS)
        data = response.json()
        
        # Check if 'articles' is in the response
        if 'news' in data and 'articles' in data['news']:
            return data['news']['articles']
        else:
            return [{"author": "Unknown", "title": "N/A", "description": "No news available"}]
    except Exception as e:
        return [{"author": "Unknown", "title": "N/A", "description": f"Error fetching news data: {str(e)}"}]

infoNews = get_news_info()

app.layout = html.Div(children=[

    html.H1(children="WeatherAPI"),
    
    html.H2(children=f"The weather Today"),
    # Display date, time, and weather info at the top of the dashboard
    html.Div([
        html.H3(f"Date: {infoWeather['date']}"),
        html.H3(f"Time: {infoWeather['time']}"),
        html.H3(f"Weather in {infoWeather['weather']['city']}: {infoWeather['weather']['temperature']} °C, {infoWeather['weather']['description']}"),
    ], style={'marginBottom': 20}),
    
    # Display date, time, and weather info at the top of the dashboard
    html.H2(children="Latest News"),
    html.Div([
        html.Div([
            html.H4(f"Title: {article['title']}"),
            html.P(f"Author: {article['author']}"),
            html.P(f"Description: {article['description']}"),
        ], style={'marginBottom': 20}) 
        for article in infoNews  # Loop over each article in the news response
    ]),

     # Navigation Links using html.A to redirect to FastAPI routes
    html.Div([
        html.A('Home', href='/'),  # Redirect to FastAPI's home route
        " | ",
        html.A('Logout', href='/logout')  # Redirect to FastAPI's logout route
    ], style={'marginTop': 20})   
])

# Expose the Flask server to integrate with FastAPI
server = app.server