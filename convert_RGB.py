%matplotlib inline
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import json
import pylab
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
data_name = 'train'
with open ("mask_train_all.txt") as anns_file:
    anns= json.load(anns_file)

num = len(anns)

for i in range (0, 1):
    with open('{}_bbox/{}_bbox_{}_{}_{}.jpg'.format(data_name, data_name, i, anns[i]['image_id'], anns[i]['sub_id'])) as img_file:
        I = io.imread(img_file)
    plt.imshow(I)
    plt.axis('off')
    coco.showAnns(anns[i])