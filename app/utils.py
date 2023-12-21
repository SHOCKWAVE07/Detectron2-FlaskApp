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
from detectron2.data import MetadataCatalog

from PIL import Image

def perform_instance_segmentation(image, output_format='png'):
    cfg = get_cfg()

    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.DEVICE = "cpu"
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

    predictor = DefaultPredictor(cfg)

    img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    outputs = predictor(img[..., ::-1])

    MetadataCatalog.get(cfg.DATASETS.TRAIN[0])

    v = Visualizer(img[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
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






