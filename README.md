# Symphony ROS


## Overview

**Symphony** is a line of collaborative manipulators (cobots) developed by **PULLON Robotics Inc.**. These versatile robotic arms are designed for seamless integration into a wide range of industrial and research environments, offering safe and efficient automation solutions.

This ROS1 package provides essential drivers, interfaces, and control functionality for Symphony manipulators, allowing you to easily integrate them into existing ROS-based systems. Whether you are developing new applications, conducting research, or automating production lines, our package simplifies the process of getting your Symphony robot up and running in no time.

<!-- ![flagship](/src/.image/symphony_flagship2.png){: width="70%" } -->
<img src="/src/.image/symphony_flagship2.png" alt="flagship" width="70%">


## Installation
#### Requirement
##### ros dependency package
```
sudo apt install ros-noetic-rqt* \
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
```
##### python package
```
conda create -n puloon python==3.7

conda activate puloon

#catkin_make를 위해 필요
pip install empy==3.3.2
pip install catkin_pkg


pip install rospkg
pip install PyQt5
pip install PySide2
pip install defusedxml

# reinstall protobuf 
pip uninstall protobuf
conda install -c conda-forge protobuf=3.6.1
```
#### Build
```
cd symphony_ros
catkin_make
```
```
source devel/setup.bash
```

## Usage
#### symphony_description
##### only symphony
```
roslaunch symphony_description symphony_description.launch symphony_type:=symphony5
```
![symphony_description.png](/src/.image/symphony_description.png)
##### with gripper
```
roslaunch symphony_description symphony_description.launch symphony_type:=symphony5 gripper:=robotiq_2f
```
![symphony_description_with_gripper.png](/src/.image/symphony_desciption_with_gripper.png)

#### symphony_moveit
##### only symphony
```
roslaunch symphony_moveit symphony_moveit.launch symphony_type:=symphony5
```
![symphony_moveit.png](/src/.image/symphony_moveit.png)
##### with gripper
```
roslaunch symphony_moveit symphony_moveit.launch symphony_type:=symphony5 gripper:=robotiq_2f
```
![symphony_moveit_gripper.png](/src/.image/symphony_moveit_gripper.png)

##### pick and place example
After execute one of two options above
```
rosrun symphony_moveit Pick_Place2.py
```
![symphony_moveit_pnp.png](/src/.image/symphony_moveit_pnp.png)



#### symphony_gazebo
##### only symphony
```
roslaunch symphony_gazebo symphony_gazebo.launch symphony_type:=symphony5
```
![symphony_gazebo.png](/src/.image/symphony_gazebo.png)
##### with gripper
```
roslaunch symphony_gazebo symphony_gazebo.launch symphony_type:=symphony5 gripper:=robotiq_2f
```
![symphony_gazego_gripper.png](/src/.image/symphony_gazebo_gripper.png)





#### symphony_gazebo + moveit
##### only symphony
```
roslaunch symphony_gazebo symphony_gazebo.launch symphony_type:=symphony5
```
```
roslaunch symphony_moveit symphony_moveit_gazebo.launch symphony_type:=symphony5
```
![symphony_gazebo_moveit.png](/src/.image/symphony_gazebo_moveit.png)
##### with gripper
```
roslaunch symphony_gazebo symphony_gazebo.launch symphony_type:=symphony5 gripper:=robotiq_2f
```
```
roslaunch symphony_moveit symphony_moveit_gazebo.launch symphony_type:=symphony5 gripper:=robotiq_2f

```
![symphony_gazebo_moveit_gripper.png](/src/.image/symphony_gazebo_moveit_gripper.png)







#### symphony_gazebo pick and place example
```
roslaunch symphony_pnp symphony_pnp_env.launch symphony_type:=symphony5 gripper:=robotiq_2f
```
```
roslaunch symphony_pnp symphony_pnp.launch
```
![symphony_gazebo_pnp.png](/src/.image/symphony_gazebo_pnp.png)  
  
## Docker
#### install docker 
Please refer to the link below  
[Docker desktop](https://www.docker.com/get-started/)  
[Docker CLI](https://docs.docker.com/engine/install/ubuntu/)  

#### go to symphony_ros directory
```
cd ~/symphony_ws
```
#### build docker file
```
docker build -t symphony-ros1 .
```
#### setting for docker gui
```
xhost +local:docker
```
#### create docker container
```
docker run -d --name symphony-ros1 -it\
  -v /dev:/dev \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $HOME/.Xauthority:/root/.Xauthority:rw \
  -v /etc/nv_tegra_release:/etc/nv_tegra_release \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  --net host \
  symphony-ros1 \
  /bin/bash
```
#### execute new docker terminal
```
docker exec -it symphony-ros1 bash
```
#### build and excute in docker container
```
cd ~/symhpony_ws
catkin_make
source devel/setup.bash
```

