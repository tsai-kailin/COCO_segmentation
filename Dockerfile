FROM gcr.io/tensorflow/tensorflow:latest-gpu
MAINTAINER Katherine Tsai (karenta0317@gmail.com)

# Update aptitude with new repo
RUN apt-get update


RUN apt-get install python-tk -y --no-install-recommends  
# install python package
RUN  pip install \
	scikit-image \
	cython

# copy data in the current working dir to the app/ dir in the container
RUN mkdir /root/app  
COPY load.py /root/app/
COPY combine_json.py /root/app/
COPY convert_RGB.py /root/app/
COPY mask_train_all.txt /root/app/
COPY tool /root/app/

WORKDIR "/root/app"



