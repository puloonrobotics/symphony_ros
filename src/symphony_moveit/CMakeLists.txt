cmake_minimum_required(VERSION 2.8.3)
project(symphony_moveit)

find_package(catkin REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  rospy
  moveit_commander
  std_msgs
)

catkin_package()

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

## Python 스크립트 설치
catkin_install_python(PROGRAMS src/Pick_Place.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

catkin_install_python(PROGRAMS src/Pick_Place2.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})