from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv
import os 

load_dotenv()


CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=os.getenv("ROBOFLOW_API_KEY")
)

def get_max_confidence_category(result):
    predictions = result["predictions"]
    
    # Find the category with maximum confidence
    max_category = max(predictions, key=lambda k: predictions[k]["confidence"])
    
    return max_category, predictions[max_category]["confidence"]

image_url = "/Users/ravichandera/april_onwards/Dharti---Drishti/storage_service/soil_images/image.png"
result = CLIENT.infer(image_url, model_id="soil-type-ladmq/6")
print(result)
category, confidence = get_max_confidence_category(result)

print("category",category)    
print("confidence", confidence)