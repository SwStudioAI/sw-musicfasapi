#!/usr/bin/env python3

import os
import uvicorn

# Set environment variables for development
os.environ.setdefault("PROJECT_NAME", "SW Music Fast API")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "changethis")
os.environ.setdefault("POSTGRES_DB", "sw_music_api")
os.environ.setdefault("FIRST_SUPERUSER", "admin@sw-music.com")
os.environ.setdefault("FIRST_SUPERUSER_PASSWORD", "changethis")
os.environ.setdefault("SECRET_KEY", "changethis")

# Google Cloud / Vertex AI
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "sw-musicfastapi")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("VERTEX_AI_MODEL", "gemini-2.5-flash-lite")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"]
    )
