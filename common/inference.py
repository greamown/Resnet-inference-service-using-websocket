import torch, cv2, onnx
import numpy as np
import onnxruntime as rt
from .utils import WEIGHTS_PTAH, LABEL_NAME_PATH, read_txt
from torchvision.transforms import Normalize

def preprocess_image(img):
    img = cv2.resize(img, (224,224), cv2.INTER_NEAREST)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/255
    norm = Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    result = norm(torch.from_numpy(img).transpose(0,2).transpose(1,2))
    return np.array(result, dtype=np.float32)

def load_onnx():
    onnx_model = onnx.load(WEIGHTS_PTAH)
    sess = rt.InferenceSession(WEIGHTS_PTAH)

    input_all = [node.name for node in onnx_model.graph.input]
    input_initializer = [
        node.name for node in onnx_model.graph.initializer
    ]
    net_feed_input = list(set(input_all) - set(input_initializer))
    assert len(net_feed_input) == 1

    sess_input = sess.get_inputs()[0].name
    sess_output = sess.get_outputs()[0].name
    
    return sess, sess_input, sess_output
    
def onnx_infer(sess, sess_input, sess_output, preprocessed_images):
    onnx_result = sess.run([sess_output], {sess_input: preprocessed_images})[0]
    pred = onnx_result.squeeze()
    pred = softmax(pred)
    return pred

def softmax(x):
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x

def read_classes_name():
    classes = read_txt(LABEL_NAME_PATH)
    classes = classes.split("\n")
    return classes
        