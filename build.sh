#!/usr/bin/env bash
# Build script for Render deployment
# Builds the React frontend and copies it into backend/static/

set -o errexit

echo ">>> Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo ">>> Installing frontend dependencies..."
cd ../frontend
npm install

echo ">>> Building frontend..."
npm run build

echo ">>> Copying build to backend/static/..."
rm -rf ../backend/static
cp -r dist ../backend/static

echo ">>> Build complete."
