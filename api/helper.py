import base64
from PIL import Image, ImageDraw
from io import BytesIO
import threading


def convert_image_to_base64(image):
    # Convert the image to base64 directly
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue())

    return image_base64


def convert_base64_to_image(base64_string):
    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(base64_string)

    # Create a BytesIO object to read the image data
    image_buffer = BytesIO(image_bytes)

    # Open the image using PIL
    image = Image.open(image_buffer)

    return image


def draw_bounding_boxes(image, bounding_boxes):
    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Define the colors for different classes
    colors = {1: "red", 2: "blue"}

    # Define a helper function for drawing a single bounding box
    def draw_single_bbox(bbox):
        xmin = bbox["xmin"]
        ymin = bbox["ymin"]
        xmax = bbox["xmax"]
        ymax = bbox["ymax"]
        class_id = bbox["class"]

        # Get the color for the class
        color = colors.get(class_id, "green")

        # Acquire the lock to safely access the draw object
        # Draw the bounding box rectangle
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=color, width=2)

        # Add the class label
        label = bbox["name"]
        draw.text((xmin, ymin), label, fill=color)

    # Create a list to store the threads
    threads = []

    # Iterate over the bounding boxes
    for bbox in bounding_boxes:
        # Create a thread for each bounding box
        thread = threading.Thread(target=draw_single_bbox, args=(bbox,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return image
