# AI Services API

A FastAPI application that provides AI-powered services, including image generation and weather reports.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Generate Image

-   **Endpoint:** `POST /generate-image/`
-   **Description:** Generates an image based on a text prompt.
-   **Request Body:**
    ```json
    {
      "prompt": "A futuristic city with flying cars"
    }
    ```
-   **Response:**
    ```json
    {
      "image_url": "http://localhost:8000/static/generated_xxxxxxxx.png"
    }
    ```

### Get Weather

-   **Endpoint:** `GET /weather/{city}`
-   **Description:** Gets the weather report for a specific city.
-   **Path Parameter:** `city` (e.g., `/weather/London`)
-   **Response:**
    ```json
    {
      "wheather": "Mostly Cloudy, 18°C (64°F). Feels like 17°C. Humidity 78%. Light breeze from the East. Low chance of rain.",
      "hour": "03:30 PM COT"
    }
    ```

### Edit Image

-   **Endpoint:** `POST /edit-image/`
-   **Description:** Edits an image based on a prompt and image URL.
-   **Request Body:**
    ```json
    {
      "url": "http://path/to/your/image.png",
      "prompt": "Make the sky blue"
    }
    ```
-   **Response:**
    ```json
    {
      "image_url": "Edited image URL"
    }
    ```
