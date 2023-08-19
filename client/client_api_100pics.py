import sys, requests, os, logging, time
from argparse import ArgumentParser, SUPPRESS

SERVER_URL = "http://192.168.1.1:3000/api/infer"
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

    return image_data

def main(args):
    # try:
        total = {}
        total.update({"cost":[]})
        total.update({"fps":[]})
        # Check type of path
        if os.path.isdir(args.path):
            file_list = [ os.path.join(args.path, file) for file in os.listdir(args.path)]
            files = []
            for file in file_list:
                encoded = encode_image(file)
                files.append(("files", (file, encoded, "image/{}".format(os.path.splitext(file)[-1][1:]))))
                start = time.time()
                result = requests.request("POST", SERVER_URL, files=files)
                final = time.time()
                cost = final - start
                if "2" in str(result.status_code):
                    print(result.json())
                    total["cost"].append(cost)
                    print("Cost: {} s".format(cost))
                    fps = 1/cost
                    print("FPS: {}".format(fps))
                    total["fps"].append(fps)
                else:
                    print(str(result.status_code))
            print("-"*100)
            total_cost = sum(total["cost"])/len(total["cost"])
            print("Total cost:{} s".format(total_cost))
            print("Total FPS:{}".format(1/total_cost))

        elif os.path.isfile(args.path):
            file = args.path 
            files = []
            encoded = encode_image(file)
            files.append(("files", (file, encoded, "image/{}".format(os.path.splitext(file)[-1][1:]))))
            start = time.time()
            result = requests.request("POST", SERVER_URL, files=files)
            final = time.time()
            cost = final - start
            print(result)
            total["cost"].append(cost)
            print("Cost: {} s".format(cost))
            fps = 1/cost
            print("FPS: {}".format(fps))
            total["fps"].append(fps)
            print("-"*100)
            total_cost = sum(total["cost"])/len(total["cost"])
            print("Total cost:{} s".format(total_cost))
            print("Total FPS:{}".format(1/total_cost))

    # except Exception as e:
    #     logging.error(e)

if __name__ == '__main__':
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)