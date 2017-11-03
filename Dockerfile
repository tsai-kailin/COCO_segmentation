FROM gcr.io/tensorflow/tensorflow:latest-gpu
MAINTAINER Katherine Tsai (karenta0317@gmail.com)

# Update aptitude with new repo
RUN apt-get update && apt-get install -y --no-install-recommends\
	apt-utils \
	bash-completion \
	build-essential \
	git \
	vim


RUN apt-get install python-tk -y --no-install-recommends  
# install python package
RUN  pip install \
	scikit-image \
	cython
RUN git clone https://github.com/cocodataset/cocoapi.git \
&& cd cocoapi/PythonAPI \
&& make install

# copy data in the current working dir to the app/ dir in the container
RUN mkdir /app  
COPY load.py /app/
COPY combine_json.py /app/
COPY convert_mask.py /app/
COPY mask_val2017_all.txt /app/


WORKDIR "/app"



