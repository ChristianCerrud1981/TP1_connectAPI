#!/bin/bash

# Move into the correct directory where the FastAPI app is located
cd TP1_connectAPI

# Run the FastAPI + Dash app using Uvicorn
uvicorn fastapi_app.main:app --host 127.0.0.1 --port 8002 --workers 1