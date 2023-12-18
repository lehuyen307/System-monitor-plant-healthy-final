from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model.classification import (
    tomato_clasifier,
    leave_clasifier,
    predict,
    batch_predict,
)
from model.object_detection import (
    tomato_detector,
    leave_detector,
    predict as detect,
)
from thread import ThreadWithReturnValue
from helper import (
    draw_bounding_boxes,
    convert_image_to_base64,
    convert_base64_to_image,
)


from data_model import ImageRequest


USE_SECOND_CLASSIFICATION = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "PUT", "DELETE", "OPTION", "GET"],
    allow_headers=["*"],
)

tomato_class_mapping = {0: "Defective", 1: "Fresh", 2: "Immature"}
leave_class_mapping = {
    0: "Tomato Early blight leaf",
    1: "Tomato Septoria leaf spot",
    2: "Tomato leaf bacterial spot",
    3: "Tomato leaf late blight",
    4: "Tomato leaf mosaic virus",
    5: "Tomato leaf yellow virus",
    6: "Tomato leaf",
    7: "Tomato mold leaf",
}


@app.post("/classification/tomato")
def classify_tomato(req: ImageRequest):
    base64_img = req.image

    result = predict(base64_img, tomato_clasifier)

    # Code for classifying tomato
    return {"result": str(result)}


@app.post("/classification/tomato_leave")
def classify_tomato_leave(req: ImageRequest):
    base64_img = req.image

    result = predict(base64_img, leave_clasifier)
    # Code for classifying tomato
    return {"result": str(result)}


@app.post("/object_detection/tomato")
def detect_tomato(req: ImageRequest):
    base64_img = req.image

    results = detect(base64_img, tomato_detector)
    # Code for detecting tomatoes
    return {"result": results}


@app.post("/object_detection/tomato_leave")
def detect_tomato_leave(req: ImageRequest):
    base64_img = req.image

    image = convert_base64_to_image(base64_img)

    results = detect(image, leave_detector)
    # Code for detecting tomatoes
    return {"result": results}


@app.post("/object_detection/tomato_leave")
def detect_tomato_leave(req: ImageRequest):
    base64_img = req.image

    image = convert_base64_to_image(base64_img)

    results = detect(image, leave_detector)
    # Code for detecting tomatoes
    return {"result": results}


@app.post("/object_detection/combine")
def combine_detect(req: ImageRequest):
    base64_img = req.image

    image = convert_base64_to_image(base64_img)

    tomato = ThreadWithReturnValue(target=detect, args=(base64_img, tomato_detector))

    tomato.start()

    leave = ThreadWithReturnValue(target=detect, args=(base64_img, leave_detector))

    leave.start()

    tomato_result = tomato.join()
    leave_result = leave.join()

    if USE_SECOND_CLASSIFICATION:
        crop_tomato = []

        for obj in tomato_result:
            xmin = obj["xmin"]
            ymin = obj["ymin"]
            xmax = obj["xmax"]
            ymax = obj["ymax"]
            cropped_object = image.crop((int(xmin), int(ymin), int(xmax), int(ymax)))
            crop_tomato.append(cropped_object)

        if len(crop_tomato) > 0:
            tomato_classificaiton = batch_predict(crop_tomato, tomato_clasifier)
            tomato_classificaiton = [
                tomato_class_mapping[i] for i in tomato_classificaiton
            ]

            for i in range(len(tomato_result)):
                tomato_result[i]["name"] = tomato_classificaiton[i]

        # crop_leave = []

        # for obj in leave_result:
        #     xmin = obj["xmin"]
        #     ymin = obj["ymin"]
        #     xmax = obj["xmax"]
        #     ymax = obj["ymax"]
        #     cropped_object = image.crop((int(xmin), int(ymin), int(xmax), int(ymax)))
        #     crop_leave.append(cropped_object)

        # if len(crop_leave) > 0:
        #     leave_classificaiton = batch_predict(crop_leave, leave_clasifier)

        #     leave_classificaiton = [
        #         leave_class_mapping[i] for i in leave_classificaiton
        #     ]

        #     for i in range(len(leave_result)):
        #         leave_result[i]["name"] = leave_classificaiton[i]

    tomato_result.extend(leave_result)

    bbox_image = draw_bounding_boxes(image, tomato_result)

    bbox_image = bbox_image.resize((400, 400))

    return {
        "result": tomato_result,
        "bbox_image": convert_image_to_base64(bbox_image),
    }
    

@app.post("/object_detection/cam")
def combine_detect(req: ImageRequest):
    base64_img = req.image

    image = convert_base64_to_image(base64_img)

    tomato = ThreadWithReturnValue(target=detect, args=(base64_img, tomato_detector))

    tomato.start()

    leave = ThreadWithReturnValue(target=detect, args=(base64_img, leave_detector))

    leave.start()

    tomato_result = tomato.join()
    leave_result = leave.join()

    tomato_result.extend(leave_result)

    bbox_image = draw_bounding_boxes(image, tomato_result)

    bbox_image = bbox_image.resize((400, 400))

    return {
        "result": tomato_result,
        "bbox_image": convert_image_to_base64(bbox_image),
    }
