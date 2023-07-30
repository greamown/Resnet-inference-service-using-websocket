import base64, sys, websocket, os, logging, time
from argparse import ArgumentParser, SUPPRESS

SERVER_URL = "ws://0.0.0.0:5000/infer"
TIMEOUT = 3

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-p', '--path', required=True, help = "The path of inference images. you can input the folder path or the image path.")
    return parser

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        
    encoded = base64.b64encode(image_data).decode("utf-8")
    return encoded

def main(args):
    start = time.time()
    try:
        ws = websocket.create_connection(SERVER_URL, timeout=TIMEOUT)
        # Check type of path
        if os.path.isdir(args.path):
            file_list = [ os.path.join(args.path, file) for file in os.listdir(args.path)]
            for file in file_list:
                encoded = encode_image(file)
                ws.send(encoded)
                result = ws.recv()
                print(result)
                print("Cost {} s".format(time.time() - start))
        
        elif os.path.isfile(args.path):
            file = args.path 
            encoded = encode_image(file)
            ws.send(encoded)
            result = ws.recv()
            print(result)
            print("Cost {} s".format(time.time() - start))
            
        ws.close()
    except Exception as e:
        logging.error(f"Other error:{e}")

if __name__ == '__main__':
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)