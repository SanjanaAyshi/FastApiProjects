import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# ==========================================
# MIDDLEWARE 1: Process Time
# ==========================================

class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # ─── BEFORE the route runs ───
        start_time=time.time()

        # ─── Run the actual route ───
        response = await call_next(request)

        # ─── AFTER the route runs ───
        process_time=time.time() - start_time
        response.headers["x-process-time"]=f"{process_time:.4f} sec"

        return response
    
# ==========================================
# MIDDLEWARE 2: Request Logging
# ==========================================

class LoggingMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # ─── BEFORE ───
        print(f"📨 {request.method} {request.url}")

        start_time=time.time()

        # ─── Run the route ───
        response=await call_next(request)

        # ─── AFTER ───
        process_time= time.time() - start_time
        print(f"✅ Status: {response.status_code} | Time: {process_time:.4f}s")
        return response