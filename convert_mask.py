from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import os
import errno
from PIL import Image, ImageDraw
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
# select parsing file: train/val
parser.add_argument('--fname', type=str, default='val2017', required=True, help='select which file (train or val)to parse')

args = parser.parse_args()
data_name = args.fname
# create dir if not existed
def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

with open ("mask_{}_all.txt".format(data_name)) as anns_file:
    anns= json.load(anns_file)
dataDir='.'
annFile='{}/annotations/instances_{}.json'.format(dataDir,data_name)
# initialize COCO api for instance annotations
coco=COCO(annFile)

num = len(anns)
print (num)
make_sure_path_exists('{}_mask'.format(data_name))
for i in range (0, num):

    with open('{}_bbox/{}_bbox_{}_{}_{}.jpg'.format(data_name, data_name, anns[i]['top_id'],anns[i]['image_id'], anns[i]['sub_id']),'rb') as img_file:
        I = io.imread(img_file)

    nx = I.shape[1]
    ny = I.shape[0]
    img = Image.new("L", [nx, ny], 0)
    poly = np.round(np.asarray(anns[i]['segmentation'])).astype('int').reshape((-1,2))
    #poly = np.asarray(anns[i]['segmentation']).astype('int').reshape((-1,2))
    ImageDraw.Draw(img).polygon(poly.ravel().tolist(), outline=1, fill=1)
    mask = np.array(img)

    print ('save image mask {}_{}_{}'.format(anns[i]['top_id'],anns[i]['image_id'], anns[i]['sub_id']))
    plt.imsave('{}_mask/{}_mask_{}_{}_{}.png'.format(data_name, data_name, anns[i]['top_id'],anns[i]['image_id'], anns[i]['sub_id']), mask, cmap=cm.gray)