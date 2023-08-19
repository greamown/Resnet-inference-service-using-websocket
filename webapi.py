import cv2
from common import preprocess_image, onnx_infer, BATCH_SIZE, onnx_batch_infer, success_msg, error_msg
import numpy as np
from initial import sock, app, sess, sess_input, sess_output, classes
from flask import request
import uuid

@app.route("/")
def index():
    return "<h1>Hello! Resnet18 inference</h1>"

@app.route('/api/infer', methods=['POST'])
def api_infer():
    files_list = request.files
    result_dict = {}
    if files_list:
        for key in files_list.keys():
            result_dict[key] = []
            files = files_list.getlist(key)
            for file in files:
                file_data = file.read()
                np_arry = np.frombuffer(file_data, np.uint8)
                img_array = cv2.imdecode(np_arry, cv2.IMREAD_COLOR)
                input_batch = np.array(np.repeat(np.expand_dims(np.array(img_array, dtype=np.float32), axis=0), BATCH_SIZE, axis=0), dtype=np.float32)
                preprocessed_images = np.array([preprocess_image(image) for image in input_batch])
                pred = onnx_infer(sess, sess_input, sess_output, preprocessed_images)
                indices = (-pred).argsort()[:5]
                classes_list = [classes[int(idx)] for idx in indices]
                result = list(zip(classes_list, pred[indices]))
                result_dict[key].append(result)
                print(result_dict)    
    return success_msg(200, {"results":result_dict}, "Success", True)

@sock.route('/ws/infer')
def infer(ws):
    try:
        while True:
            encoded_image = ws.receive()
            if encoded_image:
                np_arry = np.frombuffer(encoded_image, np.uint8)
                img_array = cv2.imdecode(np_arry, cv2.IMREAD_COLOR)
                input_batch = np.array(np.repeat(np.expand_dims(np.array(img_array, dtype=np.float32), axis=0), BATCH_SIZE, axis=0), dtype=np.float32)
                preprocessed_images = np.array([preprocess_image(image) for image in input_batch])
                pred = onnx_infer(sess, sess_input, sess_output, preprocessed_images)
                indices = (-pred).argsort()[:5]
                classes_list = [classes[int(idx)] for idx in indices]
                result = list(zip(classes_list, pred[indices]))
                print(result)
                ws.send(result)

    except Exception as e:
        print(e)
    
@sock.route('/ws/batch/infer')
def batch_infer(ws):
    try:
        while True:
            encoded_data_list = ws.receive()
            if encoded_data_list:
                import ast
                encoded_image_list = ast.literal_eval(encoded_data_list)
                image_list = []
                for encoded_image in encoded_image_list:
                    np_arry = np.frombuffer(encoded_image, np.uint8) 
                    img_array = cv2.imdecode(np_arry, cv2.IMREAD_COLOR)
                    image_list.append(img_array)
                input_batch = np.array(image_list, dtype=np.float32)
                preprocessed_images = np.array([preprocess_image(image) for image in input_batch])
                pred = onnx_batch_infer(sess, sess_input, sess_output, preprocessed_images, classes)
                print(pred)
                ws.send(pred)

    except Exception as e:
        print(e)

@sock.route('/ws/batch/pickle/infer')
def batch_pickle_infer(ws):
    try:
        while True:
            encoded_data_list = ws.receive()
            if encoded_data_list:
                import pickle
                encoded_image_list = pickle.loads(encoded_data_list)
                image_list = []
                for encoded_image in encoded_image_list:
                    np_arry = np.frombuffer(encoded_image, np.uint8) 
                    img_array = cv2.imdecode(np_arry, cv2.IMREAD_COLOR)
                    image_list.append(img_array)
                input_batch = np.array(image_list, dtype=np.float32)
                preprocessed_images = np.array([preprocess_image(image) for image in input_batch])
                pred = onnx_batch_infer(sess, sess_input, sess_output, preprocessed_images, classes)
                print(pred)
                ws.send(pred)

    except Exception as e:
        print(e)