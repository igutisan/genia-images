from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import ia_service
import json

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


class ImageRequest(BaseModel):
    prompt: str


class ImageUpdate(BaseModel):
    url: str
    prompt: str


@app.post("/generate-image/")
async def generate_image_api(request: ImageRequest):
    try:
        image_url = ia_service.generate_image(request.prompt)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weather/{city}")
async def get_weather_api(city: str):
    try:
        weather_report_str = ia_service.get_weather(city)
        json_str_cleaned = (
            weather_report_str.strip()
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )
        weather_data = json.loads(json_str_cleaned)
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/edit-image/")
async def edit_image_api(request: ImageUpdate):
    try:
        # id = ia_service.get_image_id(request.url)
        # return id
        image_url = ia_service.edit_image(request.prompt, request.url)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
