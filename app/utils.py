import cv2
import numpy as np
import os
from PIL import Image
import io
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2 import model_zoo
from flask import current_app
import json
from detectron2.data import DatasetCatalog, MetadataCatalog

from PIL import Image
import os
import numpy as np
import json
from detectron2.structures import BoxMode


def get_sign_dicts(directory):
    classes = ['prohibitory', 'danger', 'mandatory', 'other']
    dataset_dicts = []
    img_id = 0
    for filename in [file for file in os.listdir(directory) if file.endswith('.json')]:
        json_file = os.path.join(directory, filename)
        with open(json_file) as f:
            img_anns = json.load(f)

        record = {}

        filename = os.path.join(directory, img_anns["imagePath"])

        record["file_name"] = filename
        record["image_id"] = img_id
        record["height"] = img_anns["imageHeight"]
        record["width"] = img_anns["imageWidth"]

        annos = img_anns["shapes"]
        objs = []
        for anno in annos:
            px = [a[0] for a in anno['points']]
            py = [a[1] for a in anno['points']]
            poly = [(x, y) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]

            obj = {
                "bbox": [np.min(px), np.min(py), np.max(px), np.max(py)],
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": [poly],
                "category_id": classes.index(anno['label']),
                "iscrowd": 0
            }
            objs.append(obj)
        record["annotations"] = objs
        dataset_dicts.append(record)
        img_id += 1
    return dataset_dicts



def perform_instance_segmentation(image, output_format='png'):
    cfg = get_cfg()

    cfg.merge_from_file("config.yml")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.DEVICE = "cpu"
    cfg.MODEL.WEIGHTS = os.path.join("models","model_final.pth")

    predictor = DefaultPredictor(cfg)

    img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    outputs = predictor(img[..., ::-1])
    
    v = Visualizer(img[:, :, ::-1], MetadataCatalog.get("traffic_sign_train"), scale=0.5)

    result_image = v.draw_instance_predictions(outputs["instances"].to("cpu")).get_image()

    # Convert the VisImage to a NumPy array
    result_array = np.asarray(result_image)

    # Resize the image to the target size
    pil_image = Image.fromarray(result_array)
    pil_image = pil_image.resize((680,400))  
    img_buffer = io.BytesIO()

    # Save the resized image to the buffer in the specified format
    pil_image.save(img_buffer, format=output_format.upper())

    # Get the encoded image as bytes
    encoded_image = img_buffer.getvalue()

    return encoded_image






