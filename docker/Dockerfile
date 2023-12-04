FROM ubuntu:22.04

# Configures operative system dependencies
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

# Install dependencies
RUN apt-get update -qq 
RUN echo 'Installing OS dependencies' 
RUN apt-get install -qq -y --fix-missing sudo 
RUN apt-get install -qq -y --fix-missing software-properties-common 
RUN apt-get install -qq -y --fix-missing git 
RUN apt-get install -qq -y --fix-missing unzip 
RUN apt-get install -qq -y --fix-missing wget 
RUN apt-get install -qq -y --fix-missing vim 
RUN apt-get install -qq -y --fix-missing curl 
RUN apt-get install -qq -y --fix-missing libxext-dev libxrender-dev libxslt1.1 libxtst-dev
RUN apt-get install -qq -y --fix-missing libgtk2.0-0 libcanberra-gtk-module

RUN echo 'Cleaning up' 
RUN apt-get clean -qq -y 
RUN apt-get autoclean -qq -y
RUN apt-get autoremove -qq -y 
RUN rm -rf /var/lib/apt/lists/* 
RUN rm -rf /tmp/*


# Install python3.10
RUN add-apt-repository ppa:deadsnakes/ppa 
RUN apt-get install python3.10 -y
RUN ln -s /usr/bin/python3.10 /usr/bin/python
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN rm get-pip.py
RUN apt-get install -qq -y --fix-missing python3.10-venv
RUN apt-get install -qq -y --fix-missing python3.10-tk


# Install pycharm
ENV PYCHARM /opt/pycharm
RUN mkdir $PYCHARM
RUN wget https://download-cdn.jetbrains.com/python/pycharm-community-2023.2.5.tar.gz -O - | tar xzv --strip-components=1 -C $PYCHARM
ENV PATH $PYCHARM/bin:$PATH

ENV DISPLAY host.docker.internal:0


# set no password for root
RUN passwd --delete root
# add new user: mynewuser
RUN useradd -m mynewuser -s /bin/bash
RUN usermod -aG sudo mynewuser
WORKDIR /home/mynewuser
USER mynewuser

RUN git clone https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing.git

WORKDIR /home/mynewuser/Chinese_reading_task_eeg_processing

# create new venv
RUN python -m venv eeg_dataset_env
RUN ["/bin/bash", "-c", "source ./eeg_dataset_env/bin/activate"]

# install dependencies
RUN eeg_dataset_env/bin/pip install --upgrade pip
RUN eeg_dataset_env/bin/pip install openpyxl==3.1.2
RUN eeg_dataset_env/bin/pip install mne-bids[full]==0.14
RUN eeg_dataset_env/bin/pip install psychopy==2023.2.3 --no-deps
RUN git clone https://github.com/tobiipro/g3pylib.git
RUN eeg_dataset_env/bin/pip install ./g3pylib
RUN eeg_dataset_env/bin/pip install pybv==0.7.5
RUN eeg_dataset_env/bin/pip install egi-pynetstation==1.0.1

RUN rm -rf ./g3pylib



WORKDIR /opt/pycharm/bin

USER root




