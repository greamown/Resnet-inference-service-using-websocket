from flask import Flask
from flask_sock import Sock
from flask_cors import CORS
from common import load_onnx, read_classes_name

# Initial Flask application
app = Flask(__name__)
sock = Sock(app)
CORS(app)
sess, sess_input, sess_output = load_onnx()
classes = read_classes_name()