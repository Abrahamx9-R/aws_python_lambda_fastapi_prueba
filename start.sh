#!/bin/bash
uvicorn main:app --reload --host 0.0.0.0 --port $PORT 
#python3 image_server.py