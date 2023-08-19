from flask import jsonify
import logging, os, shutil

BATCH_SIZE = 1
WEIGHTS_PTAH = "model/resnet18_pytorch-dynamic-v2.onnx"
LABEL_NAME_PATH = "model/imagenet_classes.txt"
ALLOWED_EXTENSIONS = {  "label":['txt', 'xml', 'json',
                                    "TXT", "XML", "JSON"],
                        "image":['png', 'jpg', 'jpeg', 'bmp', 
                                    "PNG", "JPG", "JPEG", "BMP"]
                    }

def error_msg(status:int, data:dict={}, text:str="", log=False):
    if log:
        logging.error(str(text))
    return response_content(status, data=data, text=text)

def success_msg(status:int, data:dict={}, text:str="", log=None):
    if log:
        logging.info(str(log))
    return response_content(status, data=data, text=text)

def response_content(status:int, data:dict={}, text:str=""):
    obj = {
            "status": status,
            "message":text,
            "data":data
        }
    return jsonify(str(obj)), status

def read_txt(path:str):
    with open(path) as f:
        return f.read()
    