import argparse
import json


parser = argparse.ArgumentParser(description='Process some integers.')
# select parsing file: train/val
parser.add_argument('--fname', type=str, default='val2017', required=True, help='select which file (train or val)to parse')
args = parser.parse_args()
data_name = args.fname

with open ('mask_{}_all.txt'.format(data_name)) as annFile:
	anns = json.load(annFile)

data_length = len(anns)

for i in range (data_length):
	print("/{}_bbox/{}_bbox_{}_{}_{}.jpg /{}_mask/{}_mask_{}_{}_{}.png".format(data_name, data_name, anns[i]['top_id'], anns[i]['image_id'], anns[i]['sub_id'], data_name, data_name, anns[i]['top_id'], anns[i]['image_id'], anns[i]['sub_id']))



