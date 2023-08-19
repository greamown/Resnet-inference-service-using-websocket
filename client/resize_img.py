import cv2, sys, os
from argparse import ArgumentParser, SUPPRESS

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-p', '--path', required=True, help = "The path of inference images. you can input the folder path or the image path.")
    args.add_argument('--width', required=True, help = "Chagne width of images.")
    args.add_argument('--height', required=True, help = "Chagne height of images.")
    
    return parser

def main(args):
    # Check type of path
    if os.path.isdir(args.path):
        file_list = [ os.path.join(args.path, file) for file in os.listdir(args.path)]
        for file in file_list:
            img = cv2.imread(file)
            img = cv2.resize(img, (int(args.height), int(args.width)), cv2.INTER_NEAREST)
            split_path = os.path.splitext(file)
            cv2.imwrite("{}-resize{}".format(split_path[0], split_path[-1]),img)
    
    elif os.path.isfile(args.path):
        file = args.path 
        img = cv2.imread(file)
        img = cv2.resize(img, (int(args.height), int(args.width)), cv2.INTER_NEAREST)
        split_path = os.path.splitext(file)
        cv2.imwrite("{}-resize{}".format(split_path[0], split_path[-1]),img)

if __name__ == '__main__':
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)