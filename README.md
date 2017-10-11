# COCO_segmentation

## Currently supported function:
1. Fetch the raw data
2. Get the bounding box
3. Get the segmentation data(.json)

## Installation
###Step 1 Docker file
This program is currently developed under docker
To run the program in you need to install the [Docker](https://www.docker.com/) and the [tensorflow Docker file(gpu version)](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/docker)
```
$ git clone https://github.com/karenta0317/COCO_segmentation.git
$ cd COCO_segmentation
$ sudo docker build -t=[your-name/image-name] .
# run the program in docker
$ sudo nvidia-docker run --rm -it --volume [/path/ you want to work under(in your computer)]:[/path in side the docker/] [your-name/image-name]
```
###Step2 Install COCOAPI
When you first acess the Docker, your will find yourself in the directory called "app"  
```
$ cd cocoapi/PythonAPI
$ make install
```
###Step3 Download Files
In our approach, we use URL to fetch the image. Thus, you need to download the COCO dtataset [annotations file](https://cocodataset.org/#download) to run our program. Please select the anotation files you want to work with and put them under the path *~/app/annotaions*

We have implemented two methods to download the dataset. The first(default) method is to download the whole [dataset.zip](https://cocodataset.org/#download) corresponding to the annotation file. This method would parse the data faster at the expense of storing large amount data(typically 20GB) on the local side. After download the image file, please unzip it and put it under the dir *~/app/*

The second approach is to download only the image you need via URL. We do not recommend this method as it would take long to complete since it fetches one image a time by posting HTML request and the round trip time is much longer than that of fetching data locally.However, if you have storage concern, please choose this method.

```
$ python load.py --m ['local/url']
```

###Step4 Run the Program
Our default anootation file is *instances_val2017.json*.
execute the program
```
$ python load.py --fname ['anotationfile'] --fid ['output file id'] --m ['mothod:local/url']
```
fname: annotation file name.
fid: parse the image data from id: 5000i to id:5000(i-1)-1
m: fetch data from local side or URL

*example*:
```
$ python load.py --fname val2017 --fid 0 --m local
```
## Directory Tree

```
COCO_segmentation
├── Dockerfile
├── tool
│   └── cocoapi*
├── run.sh
└── load.py
```
