from google import genai
from google.genai import types
from .prompt import soil_carbon_content_prompt
from dotenv import load_dotenv
import os 

load_dotenv()

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

def get_carbon_content(image_path: str):

    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents=[
        types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
        ),
        soil_carbon_content_prompt
    ]
    )
    print("carbon content response", response.text)
    return response.text

if __name__ == "__main__":

    image_path = '/Users/ravichandera/april_onwards/Dharti---Drishti/storage_service/soil_images/image.png'
    result = get_carbon_content(image_path)