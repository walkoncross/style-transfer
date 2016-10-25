"""
demo.py - Optimized style transfer pipeline for interactive demo.
"""

# system imports
import argparse
import logging
from threading import Lock
import time

# library imports
import caffe
import cv2
from skimage.transform import rescale

# local imports
from style import StyleTransfer

#added by zhaoyafei
import numpy as np
import os.path
from skimage import img_as_ubyte
from scipy.misc import imsave
##


# argparse
parser = argparse.ArgumentParser(description="Run the optimized style transfer pipeline.",
                                 usage="demo.py -s <style_image> -c <content_image>")
parser.add_argument("-s", "--style-img", type=str, required=True, help="input style (art) image")
parser.add_argument("-c", "--content-img", type=str, required=True, help="input content image")
parser.add_argument("-g", "--gpu-id", default=0, type=int, required=False, help="GPU device number")
parser.add_argument("-r", "--ratio", default="1e4", type=str, required=False, help="style-to-content ratio")
parser.add_argument("-m", "--model", default="googlenet", type=str, required=False, help="model to use")
parser.add_argument("-o", "--output", default=None, required=False, help="output path")
parser.add_argument("-i", "--init", default="content", type=str, required=False, help="initialization strategy")

model_name = 'googlenet'

# style transfer
# style workers, each should be backed by a lock
workers = {}


def gpu_count():
    """
        Counts the number of CUDA-capable GPUs (Linux only).
    """

    # use nvidia-smi to count number of GPUs
    try:
        output = subprocess.check_output("nvidia-smi -L")
        return len(output.strip().split("\n"))
    except:
        return 0

def init(model_name, n_workers=1):
    """
        Initialize the style transfer backend.
    """

    global workers
    #global model_name

    if n_workers == 0:
        n_workers = 1

    # assign a lock to each worker
    for i in range(n_workers):
        worker = StyleTransfer(model_name, use_pbar=True)
        workers.update({Lock(): worker})

def st_api(img_style, img_content, ratio=1e4, init='content', callback=None):
    """
        Style transfer API.
    """

    global workers

    # style transfer arguments
    all_args = [{"length": 360, "ratio": 2e3*ratio/1e4, "n_iter": 32, "callback": callback},
                {"length": 512, "ratio": 2e4*ratio/1e4, "n_iter": 16, "callback": callback}]

    # acquire a worker (non-blocking)
    st_lock = None
    st_worker = None
    while st_lock is None:
        for lock, worker in workers.iteritems():

            # unblocking acquire
            if lock.acquire(False):
                st_lock = lock
                st_worker = worker
                break
            else:
                time.sleep(0.1)

    # start style transfer
    #img_out = "content"
    img_out = init
    for args in all_args:
        args["init"] = img_out
        st_worker.transfer_style(img_style, img_content, **args)
        img_out = st_worker.get_generated()
    st_lock.release()

    return img_out

def main(args):
    """
        Entry point.
    """

    if args.gpu_id == -1:
        caffe.set_mode_cpu()
        print("Running net on CPU.")
    else:
        caffe.set_device(args.gpu_id)
        caffe.set_mode_gpu()
        print("Running net on GPU {0}.".format(args.gpu_id))    
    
    model_name = args.model
    # spin up a worker
    init(model_name)

    # perform style transfer
    img_style = caffe.io.load_image(args.style_img)
    img_content = caffe.io.load_image(args.content_img)
    result = st_api(img_style, img_content, np.float(args.ratio), args.init)

    # output path
    if args.output is not None:
        out_path = args.output
    else:
        out_path_fmt = (os.path.splitext(os.path.split(args.content_img)[1])[0], 
                        os.path.splitext(os.path.split(args.style_img)[1])[0], 
                        args.model, args.init, args.ratio)
        out_path = "outputs/{0}-{1}-{2}-{3}-{4}.jpg".format(*out_path_fmt)
        if os.path.exists(out_path):
            inc = 1
            while True:
                out_path = "outputs/{0}-{1}-{2}-{3}-{4}_".format(*out_path_fmt) + str(inc) + '.jpg'
                if not os.path.exists(out_path):
                    break
                else:
                    inc = inc+1

    # DONE!
    #cv2.imwrite(out_path, result)
    imsave(out_path, img_as_ubyte(result))
    print("Output saved to {0}.".format(out_path))

    # show the image
    cv2.imshow("Art", cv2.cvtColor(img_as_ubyte(result), cv2.COLOR_RGB2BGR))
    cv2.waitKey()
    cv2.destroyWindow("Art")


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    main(args)
