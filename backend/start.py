#!/usr/bin/env python3
"""
Script de inicio simple para Cloud Run.
"""
import os
import sys


import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
