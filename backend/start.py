#!/usr/bin/env python3
"""
Script de inicio simple para Cloud Run.
"""
import os
import sys


import os
import sys
print("[DEBUG] Antes del import app.main")
try:
    from app.main import app
    print("[DEBUG] Después del import app.main")
except Exception as e:
    print(f"[ERROR] Fallo import app.main: {e}")
    sys.exit(2)

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[DEBUG] Lanzando Uvicorn en puerto {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
