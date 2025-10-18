# # # main.py
# # import traceback
# # import os
# # import base64
# # from io import BytesIO
# # from fastapi import FastAPI, UploadFile, Form, HTTPException
# # from fastapi.responses import JSONResponse

# # # Importamos el error específico de la librería para una mejor depuración
# # from huggingface_hub import InferenceClient
# # from PIL import Image
# # from dotenv import load_dotenv

# # load_dotenv()

# # app = FastAPI(
# #     title="API de Generación de Imágenes v2",
# #     description="Endpoints con un modelo robusto (SDXL) y mejor manejo de errores.",
# # )

# # hf_token = os.getenv("HF_TOKEN")
# # if not hf_token:
# #     raise ValueError(
# #         "No se encontró el token de Hugging Face. Por favor, crea un archivo .env con HF_TOKEN='tu_token'"
# #     )

# # client = InferenceClient(token=hf_token)

# # # CAMBIO DE MODELO: Usamos Stable Diffusion XL. Es más potente y confiable en la API.
# # MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"


# # @app.post("/generate", summary="Generar imagen desde texto (Text-to-Image con SDXL)")
# # async def generate_image(
# #     prompt: str = Form(
# #         ..., description="La descripción de la imagen que quieres crear."
# #     ),
# # ):
# #     try:
# #         image = client.text_to_image(prompt=prompt, model=MODEL_ID)
# #     # MEJORA DE ERRORES: Capturamos el error HTTP específico de Hugging Face
# #     except HfHubHTTPError as e:
# #         # Extraemos el mensaje de error real devuelto por la API de Hugging Face
# #         error_message = e.response.json().get("error", str(e))
# #         print(f"❌ Error detallado de la API de HF: {error_message}")
# #         raise HTTPException(
# #             status_code=500, detail=f"Error de la API de Hugging Face: {error_message}"
# #         )
# #     except Exception as e:
# #         print(f"❌ Error genérico: {traceback.format_exc()}")
# #         raise HTTPException(
# #             status_code=500, detail=f"Ocurrió un error inesperado: {repr(e)}"
# #         )

# #     buffered = BytesIO()
# #     image.save(buffered, format="PNG")
# #     img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
# #     return JSONResponse(content={"prompt": prompt, "image_base64": img_b64})


# # @app.post(
# #     "/edit", summary="Editar una imagen con una descripción (Image-to-Image con SDXL)"
# # )
# # async def edit_image(
# #     file: UploadFile,
# #     prompt: str = Form(..., description="Descripción de los cambios a aplicar."),
# # ):
# #     image_bytes = await file.read()
# #     try:
# #         init_image = Image.open(BytesIO(image_bytes)).convert("RGB")
# #     except Exception:
# #         raise HTTPException(
# #             status_code=400, detail="El archivo subido no es una imagen válida."
# #         )

# #     try:
# #         edited_image = client.image_to_image(
# #             image=init_image,
# #             model="SG161222/RealVisXL_V4.0",
# #             prompt=prompt,
# #             strength=0.8,  # SDXL a menudo funciona bien con una 'strength' un poco más alta
# #         )

# #     except Exception as e:
# #         print(f"❌ Error genérico: {traceback.format_exc()}")
# #         raise HTTPException(
# #             status_code=500, detail=f"Ocurrió un error inesperado: {repr(e)}"
# #         )

# #     buffered = BytesIO()
# #     edited_image.save(buffered, format="PNG")
# #     img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
# #     return JSONResponse(content={"prompt": prompt, "image_base64": img_b64})

# from fastapi import FastAPI, Form, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.staticfiles import StaticFiles
# import replicate, base64, io, os, traceback, requests, uuid
# from PIL import Image
# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# # Cargar variables del entorno
# load_dotenv()

# # Inicializar clientes
# replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
# hf_token = os.getenv("HF_TOKEN")
# MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
# client = InferenceClient(token=hf_token)

# # Inicializar FastAPI
# app = FastAPI(title="API de generación y edición de imágenes")

# # Crear carpeta /static si no existe
# os.makedirs("static", exist_ok=True)

# # Montar carpeta para servir archivos estáticos (las imágenes generadas)
# app.mount("/static", StaticFiles(directory="static"), name="static")


# def base64_to_image(b64_string: str, filename: str = "input.png") -> str:
#     """Convierte base64 -> archivo .png y retorna ruta"""
#     image_data = base64.b64decode(b64_string)
#     image = Image.open(io.BytesIO(image_data))
#     temp_path = f"static/{filename}"
#     image.save(temp_path)
#     return temp_path


# @app.post("/generate", summary="Generar imagen desde texto")
# async def generate_image(prompt: str = Form(...)):
#     try:
#         # Generar imagen con HuggingFace
#         image = client.text_to_image(prompt=prompt, model=MODEL_ID)

#         # Guardar imagen en carpeta estática
#         filename = f"generated_{uuid.uuid4().hex}.png"
#         image_path = f"static/{filename}"
#         image.save(image_path, format="PNG", quality=80, optimize=True)

#         # Construir URL accesible
#         image_url = f"http://localhost:8000/static/{filename}"

#         return JSONResponse(content={"prompt": prompt, "image_url": image_url})

#     except Exception as e:
#         print(f"❌ Error: {traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e))
