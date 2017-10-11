from pycocotools.coco import COCO
import json
import os
import errno
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import copy
import math
import urllib2
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
# select parsing file: train/val
parser.add_argument('--fname', type=str, default='val2017', help='select which file (train or val)to parse')
# select to parse which section of the input data
parser.add_argument('--fid', type=int, default=0, nargs=1, help='section of the input file')
# select fetching method
parser.add_argument('--m', type=str, default='local', help='select fetching data method(default:local). local: use local images,url: download images via URL')

args = parser.parse_args()
data_name = args.fname
file_id = args.fid[0]
dataDir = '.'
annFile = '{}/annotations/instances_{}.json'.format(dataDir,data_name)

# create dir if not existed
def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
# process bbox and segmentation data
def parse_image(i, img, res):
	# read raw image
	I = io.imread(res)
    # get annotation Id of the images
	annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
	anns = coco.loadAnns(annIds)
	plt.imsave('{}_data/{}_raw_{}_{}.jpg'.format(data_name,data_name, i,anns[0]['image_id']),I, format="jpg")
	for j in range(0, len(anns)):
		
		# if the category is 'person'
		if anns[j]['category_id'] == 1 and len(anns[j]['segmentation']) == 1:
			# compute floor of the bbox
			bbox = copy.deepcopy(anns[j]['bbox'])
			bbox[0:2] = [math.floor(x) for x in bbox[0:2]]
			# compute ceil of the width and height of the bbox
			bbox[2:4] = [math.ceil(x)  for x in bbox[2:4]]
			# compute mask position for the new coordinate
			crop_anns = copy.deepcopy(anns[j]['segmentation'])
			crop_anns[0][0::2] = [x - bbox[0] for x in crop_anns[0][0::2]]
			crop_anns[0][1::2] = [x - bbox[1] for x in crop_anns[0][1::2]]
			crop_anns[0] = [round(x, 2) for x in crop_anns[0]]
			bbox = [int(x) for x in bbox]
			crop_img = I[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
			# save cropped image (area within bbox)
			if bbox[2] > 0 and bbox[3] > 0:
				plt.imsave('{}_bbox/{}_bbox_{}_{}_{}.jpg'.format(data_name, data_name, i, anns[j]['image_id'], j), crop_img, format="jpg")
				# append segmentatin info to the mask_list
				new_mask = {u'top_id': i,u'image_id': anns[j]['image_id'], u'category_id': 1, u'segmentation': crop_anns, u'sub_id': j}
				mask_list.append(new_mask.copy())
#				mask_list[count] = new_mask
#				add_one()
#				if count == 500:
#					update_json(mask_list)
#					print "segmentation file updated sucessfully ({}, {}) ".format(i, j)
#					with open('status.txt', 'w') as status_file:
#						status_file.write("saved image: {}, {}".format(i , j))
#					empty_list()
#					return_zero()
# update segmentation file
def update_json(new_data):
	
	with open('mask_{}_{}.txt'.format(data_name, file_id)) as old_file:
		try:
			old_data = json.load(old_file)
		except ValueError:
			old_data = []
	new_data = old_data + new_data
	with open('mask_{}_{}.txt'.format(data_name, file_id),'w') as new_file:
		json.dump(new_data, new_file)

	
# create Bbox dir
make_sure_path_exists('./{}_bbox'.format(data_name))
#original image
make_sure_path_exists('./{}_data'.format(data_name))

check_file = open('mask_{}_{}.txt'.format(data_name, file_id), 'a+').close()

# initailize COCO api for instance annotation
coco = COCO(annFile)

# get cat Ids of images with the filter 'person'
catIds = coco.getCatIds(catNms=['person'])
# get img Ids
imgIds = coco.getImgIds(catIds=catIds)

# initialize mask list
#mask_list = [{} for i in range(500)]
mask_list = []
#count = 0
#def empty_list():
#	global li
#	li = [{} for i in range(500)]

#def add_one():
#   global count   # Needed to modify global copy of globvar
#    count += 1
#def return_zero():
#	global count
#	count = 0
# num of images
num_of_image = len(imgIds)
end = min((file_id+1)*5000, num_of_image)
#process each image
#for i in range(0, num_of_image):
for i in range(file_id*5000, end):
	print ("retrieve image: {}/{} ".format(i, num_of_image))
	img = coco.loadImgs(imgIds[i])[0]
	if args.m == 'url':
	# load img from url
		try:
			res = urllib2.urlopen(img['coco_url'])
			parse_image(i, img, res)
		except urllib2.HTTPError as err:
			if err.code == 404:
				print ("page not found")
			else:
				print ("something happened! Error Code:", err.code)
	else:			
	# load img from local side
		with open ('%s/%s/%s'%(dataDir,data_name,img['file_name'])) as img_file:
			parse_image(i, img, img_file)
	
	if i % 300 == 299:
		update_json(mask_list)
		mask_list = []

update_json(mask_list)
