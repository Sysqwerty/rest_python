import logging

from ipaddress import ip_address
from typing import Callable

from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from src.api import tags, utils, notes, auth, users

logger = logging.getLogger("rate_limiter")

app = FastAPI()

# banned_ips = [
#     ip_address("192.168.1.1"),
#     ip_address("192.168.1.2"),
#     ip_address("127.0.0.2"),
# ]

allowed_ips = [
    ip_address('192.168.1.0'),
    ip_address('172.16.0.0'),
    ip_address("127.0.0.1")
]


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    # if ip in banned_ips:
    #     return JSONResponse(
    #         status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"}
    #     )
    if ip not in allowed_ips:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed IP address"})
    response = await call_next(request)

    return response


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"Rate limit exceeded for '{request.client.host}' host.")
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Перевищено ліміт запитів. Спробуйте пізніше."},
    )


app.include_router(utils.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
