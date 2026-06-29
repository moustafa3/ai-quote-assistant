from fastapi import FastAPI

app = FastAPI(
    title="AI Quote Assistant",
    description="A FastAPI prototype for an AI-powered quote generation assistant.",
    version="0.1.0",
)


@app.get("/api/v1/health")
def health_check() -> dict[str, str]:
    """
    Check if the API is running correctly.
    """
    return {
        "status": "ok",
        "service": "ai-quote-assistant",
    }