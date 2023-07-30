import base64, cv2
from common import preprocess_image, onnx_infer, BATCH_SIZE
import numpy as np
from initial import sock, app, sess, sess_input, sess_output, classes

@app.route("/")
def index():
    return "<h1>Hello! Resnet18 inference</h1>"

@sock.route('/infer')
def infer(ws):
    try:
        while True:
            encoded_image = ws.receive()
            if encoded_image:
                image_data = base64.b64decode(encoded_image)
                encode_image = np.asarray(bytearray(image_data), dtype='uint8')
                img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)
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