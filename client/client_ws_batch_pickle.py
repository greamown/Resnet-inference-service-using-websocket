import base64, sys, websocket, os, logging, time
from argparse import ArgumentParser, SUPPRESS
import pickle

SERVER_URL = "ws://192.168.1.1:3000/ws/batch/pickle/"
TIMEOUT = 3

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-p', '--path', required=True, help = "The path of inference images. you should input the folder path.")
    args.add_argument('--batch', required=True, help = "Input batch size.")
    return parser

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        
    return image_data

def main(args):
    try:
        ws = websocket.create_connection(SERVER_URL, timeout=TIMEOUT)
        total = {}
        total.update({"cost":[]})
        total.update({"fps":[]})
        # Check type of path
        if os.path.isdir(args.path):
            file_list = [ os.path.join(args.path, file) for file in os.listdir(args.path)]
            batch = 0
            file_code_list = []
            for file in file_list:
                encoded = encode_image(file)
                file_code_list.append(encoded)
                batch += 1
                if len(file_code_list) == int(args.batch):
                    start = time.time()
                    bin_list = pickle.dumps(file_code_list)
                    # print(bin_list)
                    ws.send_binary(bin_list)
                    # ws.send(str(file_code_list))
                    result = ws.recv()
                    # print(result)
                    final = time.time()
                    cost = final - start
                    total["cost"].append(cost)
                    # print("Cost: {} s".format(cost))
                    if cost != 0:
                        fps = 1/cost
                        # print("FPS: {}".format(fps))
                        total["fps"].append(fps)
                    file_code_list = []
            print("-"*100)
            total_cost = sum(total["cost"])/len(total["cost"])
            print("Avg cost:{} s".format(total_cost))
            print("Avg FPS:{}".format(1/total_cost))
            total_cost_pic = total_cost/int(args.batch)
            print("Avg cost/pic:{} s".format(total_cost_pic))
            print("Avg FPS/pic:{}".format(1/total_cost_pic))

        ws.close()
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)