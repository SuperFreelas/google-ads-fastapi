import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import google_ads_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("google-ads-mcp-api")

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Google Ads MCP API",
    description="API for Google Ads Management Control Panel",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(google_ads_router.router)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify if the API is running
    """
    return {"status": "healthy", "version": "1.0.0"}

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that redirects to the API documentation
    """
    return {
        "message": "Google Ads MCP API is running",
        "documentation": "/docs",
        "openapi": "/openapi.json",
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    
    uvicorn.run("main:app", host=host, port=port, reload=True) 