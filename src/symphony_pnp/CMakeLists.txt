cmake_minimum_required(VERSION 2.8.3)
project(symphony_pnp)

add_compile_options(-std=c++11)
add_definitions(-D_OS_UNIX)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs message_generation actionlib_msgs actionlib moveit_ros_planning_interface moveit_visual_tools)
find_package(Eigen3 REQUIRED)
## Declare a catkin package
catkin_package()

include_directories(SYSTEM ${EIGEN3_INCLUDE_DIRS})
include_directories(include ${catkin_INCLUDE_DIRS})
include_directories(include ${PROJECT_SOURCE_DIR}/src)

# add_executable(khu_moveit_sample src/move_it/khu_moveit_sample.cpp)
# add_dependencies(khu_moveit_sample ${catkin_EXPORTED_TARGETS})
# target_link_libraries(khu_moveit_sample ${catkin_LIBRARIES} )

add_executable(p_n_p src/move_it/p_n_p.cpp)
add_dependencies(p_n_p ${catkin_EXPORTED_TARGETS})
target_link_libraries(p_n_p ${catkin_LIBRARIES} )

# Install


## Mark executables and/or libraries for installation
install(TARGETS 
    p_n_p
    ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

