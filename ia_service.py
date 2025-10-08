from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os, uuid, dotenv

dotenv.load_dotenv()


def generate_image(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt],
    )
    filename = f"generated_{uuid.uuid4().hex}.png"
    image_path = f"static/{filename}"
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(image_path)
    image_url = f"http://localhost:8000/static/{filename}"
    return image_url


def get_weather(city: str):
    systemPrompt = f"Generate a weather report for {city} updated. please return this response {{wheather, date(with hour please)}}"
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[systemPrompt],
    )
    return response.text


def edit_image(prompt, image_url):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    id = get_image_id(image_url)
    image = Image.open(f"/home/igutisan/University/test/static/{id}.png")
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt, image],
        # config=types.GenerateImagesConfig(number_of_images=1),
    )
    filename = f"modified_{uuid.uuid4().hex}.png"
    image_path = f"static/{filename}"
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(image_path)
    image_url = f"http://localhost:8000/static/{filename}"
    return image_url


def get_image_id(image_url):
    return image_url.split("/")[-1].split(".")[0]
