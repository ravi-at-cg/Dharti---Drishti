from google import genai
from google.genai import types
from prompt import soil_carbon_content_prompt
from dotenv import load_dotenv
import os 

load_dotenv()

with open('/Users/ravichandera/april_onwards/Dharti---Drishti/storage_service/soil_images/image.png', 'rb') as f:
    image_bytes = f.read()

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

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

print(response.text)