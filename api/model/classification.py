import base64
import numpy as np
from PIL import Image
from io import BytesIO

from keras.models import load_model

tomato_clasifier = load_model("weights/classification/tomato.h5")

leave_clasifier = load_model("weights/classification/leave.h5")


def predict(base64_image, model):
    # Convert base64 image to PIL Image object
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))

    # Preprocess the image
    image = image.resize(
        (150, 150)
    )  # Resize to match the input size of the model
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make prediction
    predictions = model.predict(image)

    # Get the predicted class label
    class_index = np.argmax(predictions[0])

    return class_index


def batch_predict(pil_images, model):
    # Preprocess the images
    processed_images = []
    for image in pil_images:
        image = image.resize((200, 200))  # Resize to match the input size of the model
        image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
        processed_images.append(image)

    # Convert the list of processed images to a numpy array
    batch = np.array(processed_images)

    # Make predictions on the batch of images
    predictions = model.predict(batch)

    # Get the predicted class labels for each image
    class_indices = np.argmax(predictions, axis=1)
    

    return class_indices