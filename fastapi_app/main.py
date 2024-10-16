import sys, os
#Add the root directory to the syspatch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
from dash_app import app as app_dash


#create app
app = FastAPI()

#Define the paths

#Get the absolute path to the templates directory
templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

#Get the absolute path to the static directory
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

#serve static files
app.mount("/static", StaticFiles(directory=static_dir))

#set up Jinja2 template for rendering HTML files
templates = Jinja2Templates(directory=templates_dir)

# In-memory user storage for login
users = {'admin': "password"}

#Define routes
@app.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
async def home_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...),password: str = Form(...)):
    if username in users and users[username] == password:
        #Redirect to the dashboard generated with dash upon success
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(key="Authorization", value="Bearer Token", httponly=True)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credential"})

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url='/login')
    response.delete_cookie("Authorization")
    return response
    
#Mount the Dash under the /dashboard path 
app.mount("/dashboard", WSGIMiddleware(app_dash.server))

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001, workers=1)