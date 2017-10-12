import skimage.io as io
import numpy as np
import argparse
import json
import os, os.path
import glob
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description='Process some integers.')
# enter the groundtruth file path
parser.add_argument('--gdir', type=str, default='./val2017_mask', help='enter the ground truth mask dir path')
# enter the target file path
parser.add_argument('--tdir', type=str, required=True, help='enter the target mask dir path or the polygon .json file path')
# target datatype: polygon / mask
parser.add_argument('--dtype', type=str, required=True, help='enter "p" to process polygon coordinate from the target file, enter "m" to process segmentation mask')

args = parser.parse_args()
data_name = args.gdir
# cpmputer for: intersection / union
def compute_iou(gmask, tmask):	
	i = tmask * gmask
	u = tmask + gmask - i
	iou = np.sum(i) / np.sum(u)
	return iou

acc_iou = 0.
total_num = 0

# check the number of groundtruth files
gfile_count =  len([name for name in os.listdir(args.gdir) if os.path.isfile(os.path.join(args.gdir, name))])
# process polygon data type
if args.dtype == 'p':
	# read target file
	with open (args.tdir) as p_file:
		anns = json.load(p_file)
	# check if #groundtruth == #target
	if gfile_count == len(anns):
		for i in range (gfile_count):	
			# read groundtruth file
			with open (glob.glob('{}/*_mask_{}_{}_{}.png'.format(args.gdir, anns[i]['top_id'], anns[i]['image_id'], anns[i]['sub_id']))[0],'rb') as gt_file:
				gt = io.imread(gt_file)
			# width & height of the image
			nx = gt.shape[1]
			ny = gt.shape[0]
			# initialize new mask
			img = Image.new("L", [nx, ny], 0)
			# from polygon to binary mask
			poly = np.round(np.asarray(anns[i]['segmentation'])).astype('int').reshape((-1,2))
			ImageDraw.Draw(img).polygon(poly.ravel().tolist(), outline=1, fill=1)
			# convert mask to ndarray
			tmask = np.array(img)
			gmask = gt[:,:,0] / 255
			# compute iou
			iou = compute_iou(gmask, tmask)
			print ('process {}/{}'.format(i, gfile_count), 'iou = ', iou)
			acc_iou += iou
	else:
		raise ValueError("the number of groundtruth files is not equal to the number of target files")
# process mask datatype
else:
	tfile_count = len([name for name in os.listdir(args.tdir) if os.path.isfile(os.path.join(args.tdir, name))])
	# check if #groundtruth == #target
	if gfile_count == tfile_count:
		for i in range (gfile_count):
			with open (sorted(glob.glob('{}/*.png'.format(args.gdir)))[i], 'rb') as gt_file:
				gt = io.imread(gt_file)
			with open (sorted(glob.glob('{}/*.png'.format(args.tdir)))[i], 'rb') as t_file:
				t = io.imread(t_file)
			iou = compute_iou(gt[:,:,0] / 255, t[:,:,0] / 255)
			acc_iou += iou
			print ('process {}/{}'.format(i, gfile_count), 'iou = ', iou)
	else:
		raise ValueError("the number of groundtruth files is not equal to the number of target files")
print ('total number of files: ', gfile_count)
print ('mean IOU: ', acc_iou/gfile_count)
