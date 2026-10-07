FROM ros:noetic-ros-base-focal

# install basic package
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    lsb-release \
    build-essential \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# install ros packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-noetic-robot=1.5.0-1* \
    ros-noetic-rqt* \
    ros-noetic-moveit* \
    ros-noetic-gazebo-ros-control \
    ros-noetic-joint-state-controller \
    ros-noetic-effort-controllers \
    ros-noetic-position-controllers \
    ros-noetic-ros-controllers \
    ros-noetic-ros-control \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-joint-state-publisher \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-industrial-robot-client \
    ros-noetic-ompl \
    ros-noetic-moveit-ros \
    ros-noetic-moveit-servo \
    ros-noetic-moveit-planners \
    ros-noetic-moveit-simple-controller-manager \
    ros-noetic-warehouse-ros-mongo \
    ros-noetic-spacenav-node \
    spacenavd \
    && rm -rf /var/lib/apt/lists/*

# install conda
SHELL ["/bin/bash", "-c"]

RUN mkdir -p /root/miniconda3 \
  && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh \
  && bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3 \
  && rm /root/miniconda3/miniconda.sh \
  && source /root/miniconda3/bin/activate \
  && conda init --all

# .bashrc update
RUN echo "eval \"\$(conda shell.bash hook)\"" >> /root/.bashrc && \
    echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc && \
    echo "conda activate puloon" >> /root/.bashrc
    # echo "export PATH=\"/root/miniconda3/bin:\$PATH\"" >> /root/.bashrc && \

ENV PATH=/root/miniconda3/bin:$PATH

# create symphony env
RUN source /root/.bashrc \
  && conda create -n puloon python==3.7 -y \
  && /root/miniconda3/envs/puloon/bin/pip install\
  empy==3.3.2 \
  catkin_pkg \
  rospkg \
  PyQt5 \
  PySide2 \
  defusedxml \
  pyyaml \
  numpy \
  && conda run -n puloon --no-capture-output conda remove -y protobuf || true  \
  && conda run -n puloon --no-capture-output conda install -y -c conda-forge protobuf=3.6.1

# RUN apt-get update && apt-get install -y python3-empy && rm -rf /var/lib/apt/lists/*
# RUN conda run -n puloon --no-capture-output pip install empy==3.3.2
 

# copy directory 
 
RUN cd /root \
  && mkdir -p symphony_ros/src

COPY ./src /root/symphony_ros/src/

# build package
# SHELL ["/bin/bash", "-c"]

# RUN cd /root/symphony_ws \
#   && conda activate puloon \
#   && source /opt/ros/noetic/setup.bash \
#   && conda run -n puloon --no-capture-output catkin_make
