from ai_services.soil_type.soil_type import get_soil_category
from ai_services.carbon_content.carbon_content import get_carbon_content
from ai_services.action_engine.action_engine import get_actions
from ai_services.envrionment_parameters.env_params import build_land_profile


def process_image(image_path:str, latitude:float, longitude:float, top_best_crop:int):
    soil_type, confidence = get_soil_category(image_path)
    carbon_content = get_carbon_content(image_path)
    envrionment_parameters = build_land_profile(latitude, longitude)
    actions_json = get_actions(soil_type, top_best_crop, carbon_content, envrionment_parameters)
    return actions_json

if __name__ == "__main__":
    lat = 16.5062
    lon = 80.6480
    top_best_crop = 2
    image_path = "/Users/ravichandera/april_onwards/Dharti---Drishti/storage_service/soil_images/image.png"
    output = process_image(image_path, lat, lon, top_best_crop)
    print("final output", output)
