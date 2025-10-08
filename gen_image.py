from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
import dotenv

dotenv.load_dotenv()

key = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=key)

prompt = ("change teh cat for a dog",)

image = Image.open(
    "/home/igutisan/University/test/static/generated_d3bb643c8ebd417fade01b9d1bc37a77.png"
)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt, image],
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("generated_image.png")
