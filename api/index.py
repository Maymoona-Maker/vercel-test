import os
import httpx

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def home():
    return {
        "status": "online",
        "service": "Vercel + FastAPI"
    }


@app.get("/test-codecraft")
async def test_codecraft():

    api_key = os.getenv("CODECRAFT_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="CODECRAFT_API_KEY is missing"
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "muse-spark-1.1",
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly: CODECRAFT WORKS"
            }
        ],
        "temperature": 0
    }

    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                "https://codecraftapi.com/v1/chat/completions",
                headers=headers,
                json=payload
            )

        return {
            "status_code": response.status_code,
            "codecraft_response": response.json()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )