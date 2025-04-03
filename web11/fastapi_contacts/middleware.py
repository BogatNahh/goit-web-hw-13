from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

limiter = Limiter(key_func=get_remote_address)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await limiter.check(request, call_next)
        return response
