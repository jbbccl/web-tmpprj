#!/bin/bash
cd backend/app
source activate  
uvicorn main:app --reload --port 8001 