#!/bin/bash

# Start FastAPI application in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for a few seconds to ensure FastAPI starts
sleep 5

# Start Streamlit application in the background
streamlit run app.py 