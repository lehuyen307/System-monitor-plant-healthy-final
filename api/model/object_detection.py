import base64
import torch
from PIL import Image
from io import BytesIO


tomato_detector = torch.hub.load(
    "ultralytics/yolov5", "custom", path="weights/object_detection/tomato.pt"
)

leave_detector = torch.hub.load(
    "ultralytics/yolov5", "custom", path="weights/object_detection/leave.pt"
)

leave_detector.conf = 0.3
tomato_detector.conf = 0.3


print(tomato_detector.names)
print(leave_detector.names)


# name_mapping = {
# "Tomato bacterial spot": "Bệnh chấm trùng khuẩn cà chua",
# "Tomato early blight": "Bệnh thối sớm cà chua",
# "Tomato late blight": "Bệnh thối muộn cà chua",
# "Tomato leaf mold": "Bệnh mốc lá cà chua",
# "Tomato septoria leaf spot": "Bệnh chấm lá Septoria cà chua",
# "Tomato Spider_mites Two-spotted_spider_mite": "Rận nhện hai chấm cà chua",
# "Tomato Target_Spot": "Bệnh chấm mục tiêu cà chua",
# "Tomato Tomato_Yellow_Leaf_Curl_Virus": "Bệnh virus xoăn lá vàng cà chua",
# "Tomato Tomato_mosaic_virus": "Bệnh virus khảm lá cà chua",
# "Tomato healthy": "Cà chua khỏe mạnh"
# }


def predict(base64_image, model):
    # Convert base64 image to PIL Image object
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))

    results = model([image], size=640)

    results = results.pandas().xyxy[0].to_dict("records")
    
    print(results)

    return results
