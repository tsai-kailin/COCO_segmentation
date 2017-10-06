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
###Step3 Download Annotations File
In our approach, we use URL to fetch the image. Thus, you need to download the COCO dtataset [annotations file](http://cocodataset.org/#download) to run our program. Please select the anotation files you want to work with and put them under the 
path *~/app/annotaions*
###Step4 Run the Program
Our default anootation file is *instances_val2017.json*. if you wnat to change the file please modify the code in *load.py*
```python
 dataDir = '.'  # parent directory path
 dataType = 'train2017' # annotations file
 annFile = '{}/annotations/instances_{}.json'.format(dataDir,dataType)
```
execute the program
```
$ python load.py
```
## Directory Tree

```
COCO_segmentation
├── Dockerfile
├── tool
│   └── cocoapi*
└── load.py
```
