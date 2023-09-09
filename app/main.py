from app.api.routers.pdf_router import get_pdf_router
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.config import settings


# Function to initialize the FastAPI app.
def init_app() -> FastAPI:
    app = FastAPI(title=settings.API_TITLE)
    # Include the car router.
    app.include_router(get_pdf_router())
    # Include the CORS middleware.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["OPTIONS", "GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"]
    )
    return app


# Create the FastAPI app.
app = init_app()

# Create a handler for AWS Lambda.
handler = Mangum(app)

# Start the server.
if __name__ == "__main__":
    uvicorn.run(app,
                host=settings.API_HOST,
                reload=True,
                port=settings.API_PORT,
                ssl_certfile=settings.SSL_CERT_FILE,
                ssl_keyfile=settings.SSL_KEY_FILE)
