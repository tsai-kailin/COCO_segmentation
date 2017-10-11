import json
import os

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
# select parsing file: train/val
parser.add_argument('--fname', type=str, default='val2017', required=True, help='select which file (train or val)to parse')

args = parser.parse_args()
data_name = args.fname

big_list = []
index = 0
parse_file = './mask_{}_{}.txt'.format(data_name, index)
while os.path.isfile(parse_file):
	print ('adding file {}.....'.format(parse_file))
	with open(parse_file,'r') as read_file:
		data = json.load(read_file)
	big_list = big_list + data
	index += 1	
	parse_file = './mask_{}_{}.txt'.format(data_name, index)

with open('mask_{}_all.txt'.format(data_name),'w') as write_file:
	json.dump(big_list, write_file)
