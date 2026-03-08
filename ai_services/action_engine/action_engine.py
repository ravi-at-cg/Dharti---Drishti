from groq import Groq
from dotenv import load_dotenv
import os
from datetime import datetime
from .prompt import get_suggestions_prompt

load_dotenv()

def get_actions(soil_type:str, top_best_crop:int, carbon_content: any, envrionment_parameters:dict[any, any]):

  user_parameter_input = f"""
  {get_suggestions_prompt}

  Soil type: {soil_type}

  Carbon content: {carbon_content}

  {str(envrionment_parameters)}

  Return Only Top {top_best_crop} Suggestions for given details."""

  client = Groq(api_key = os.getenv("GROQ_API_KEY"))
  completion = client.chat.completions.create(
      model="openai/gpt-oss-120b",
      messages=[
          {
              "role": "user",
              "content": user_parameter_input
          }
      ]
  )
  output = completion.choices[0].message.content
  # Store output to text file
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  # Get the project root directory (2 levels up from this file)
  current_dir = os.path.dirname(os.path.abspath(__file__))
  project_root = os.path.dirname(os.path.dirname(current_dir))
  output_dir = os.path.join(project_root, "storage_service", "model_outputs")
  os.makedirs(output_dir, exist_ok=True)
  output_path = os.path.join(output_dir, f"model_output_{timestamp}.txt")
  with open(output_path, "w") as f:
      f.write(output)
  return output

if __name__ == "__main__":
  soil_type = "Alluvial Soil"

  top_best_crop = 2

  envrionment_parameters = {
    "terrain": {
      "elevation_m": 245,
      "slope_degree": 6.8,
      "slope_percent": 11.9,
      "aspect_degree": 135,
      "aspect_direction": "SE"
    },
    "hydrology": {
      "near_waterbody": "true",
      "distance_to_waterbody_m": 320,
      "waterbody_type": "river"
    },
    "climate": {
      "avg_temperature_c": 27.4,
      "max_temperature_c": 41.2,
      "min_temperature_c": 12.5,
      "weekly_temp_averages_c": {
        "week_1": 26.8,
        "week_2": 27.3,
        "week_3": 28.1,
        "week_4": 27.5
      },
      "relative_humidity_percent": 64,
      "dew_point_c": 19.2,
      "rainfall": {
        "daily_mm": 3.4,
        "monthly_mm": 112,
        "annual_mm": 845
      },
      "rain_pattern": "monsoon_dominant",
      "rainy_days_count": 58,
      "peak_rain_month": "July"
    }
  }
  carbon_content = 0.012
  output = get_actions(soil_type, top_best_crop, carbon_content, envrionment_parameters)
  print(output)