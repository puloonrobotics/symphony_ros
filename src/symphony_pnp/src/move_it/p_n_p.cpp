// student ID: 2018100674
// name: Haneul Kim

// ROS
#include <ros/ros.h>

// MoveIt
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <cmath>
#include <iostream>
#include <moveit_msgs/CollisionObject.h>
#include <shape_msgs/SolidPrimitive.h>
#include <geometry_msgs/Pose.h>

// TF2
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>

class Location {
public:
    double x;
    double y;

    Location() {};
    Location(double x_value, double y_value) {
        x = x_value;
        y = y_value;
    }
};

class Block {
public:
    double width;
    double length;
    double height;
    double radius;
    Location location;

    Block() {}
    Block(double width_value, double length_value, double height_value, double radius_value, Location location_value) {
        width = width_value;
        length = length_value;
        height = height_value;
        radius = radius_value;
        location = location_value;
    }
};


geometry_msgs::Pose list_to_pose(double x, double y, double z, double roll, double pitch, double yaw) {
    geometry_msgs::Pose pose;
    tf2::Quaternion orientation;
    orientation.setRPY(roll, pitch, yaw);
    pose.position.x = x;
    pose.position.y = y;
    pose.position.z = z;
    pose.orientation = tf2::toMsg(orientation);

    return pose;
}

void go_to_pose_goal(moveit::planning_interface::MoveGroupInterface& move_group_interface,
    geometry_msgs::Pose& target_pose) {
    // .. _move_group_interface-planning-to-pose-goal:

    move_group_interface.setPoseTarget(target_pose);
    moveit::planning_interface::MoveGroupInterface::Plan my_plan;


    bool success = (move_group_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

    // Finally, to execute the trajectory stored in my_plan, you could use the following method call:
    // Note that this can lead to problems if the robot moved in the meanwhile.
    move_group_interface.execute(my_plan);

}

void grab_block(moveit::planning_interface::MoveGroupInterface& gripper_interface, double value) {
    ROS_INFO("gripper sample");
    moveit::planning_interface::MoveGroupInterface::Plan my_plan;

    // Next get the current set of joint values for the group.
    std::vector<double> joint_group_positions;

    joint_group_positions = gripper_interface.getCurrentJointValues();
    joint_group_positions[0] = 0;
    joint_group_positions[1] = 0;
    joint_group_positions[2] = value;
    joint_group_positions[3] = 0;
    // Now, let's modify one of the joints, plan to the new joint space goal and visualize the plan.
    gripper_interface.setJointValueTarget(joint_group_positions);
    bool success = (gripper_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
    gripper_interface.execute(my_plan);
}

// 놓는게 0임
void release_block(moveit::planning_interface::MoveGroupInterface& gripper_interface) {
    ROS_INFO("gripper sample");
    moveit::planning_interface::MoveGroupInterface::Plan my_plan;

    // Next get the current set of joint values for the group.
    std::vector<double> joint_group_positions;

    joint_group_positions = gripper_interface.getCurrentJointValues();
    joint_group_positions[0] = 0;
    joint_group_positions[1] = 0;
    joint_group_positions[2] = 0;
    joint_group_positions[3] = 0;
    // Now, let's modify one of the joints, plan to the new joint space goal and visualize the plan.
    gripper_interface.setJointValueTarget(joint_group_positions);
    bool success = (gripper_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
    gripper_interface.execute(my_plan);
}

void initial_pose(moveit::planning_interface::MoveGroupInterface& arm_interface) {
    ROS_INFO("gripper sample");
    moveit::planning_interface::MoveGroupInterface::Plan my_plan;

    // Next get the current set of joint values for the group.
    std::vector<double> joint_group_positions;

    joint_group_positions = arm_interface.getCurrentJointValues();
    // -J joint0 0.0 -J joint1 -2.03 -J joint2 1.58 -J joint3 -1.19 -J joint4 -1.58 -J joint5 0.0"
    joint_group_positions[0] = 0;
    joint_group_positions[1] = -2.03;
    joint_group_positions[2] = 1.58;
    joint_group_positions[3] = -1.19;
    joint_group_positions[4] = -1.58;
    joint_group_positions[5] = 0;
    // Now, let's modify one of the joints, plan to the new joint space goal and visualize the plan.
    arm_interface.setJointValueTarget(joint_group_positions);
    bool success = (arm_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
    arm_interface.execute(my_plan);
}

void move_block(moveit::planning_interface::MoveGroupInterface& arm_interface, moveit::planning_interface::MoveGroupInterface& gripper_interface, Block block, Location location, double value) {
    geometry_msgs::Pose target_pose1, target_pose2, target_pose3, target_pose4, target_pose5, target_pose6;

    target_pose1 = list_to_pose(0.34, 0, 0.4, M_PI, 0, M_PI / 2); // 잡는 곳 중간위치
    target_pose2 = list_to_pose(block.location.x, block.location.y, 0.4, M_PI, 0, M_PI / 2);
    target_pose3 = list_to_pose(block.location.x, block.location.y, block.height + 0.12, M_PI, 0, M_PI / 2);
    target_pose4 = list_to_pose(0, 0.3 + 0.2, 0.4, M_PI, 0, M_PI / 2); // 놓는곳 중간위치
    target_pose5 = list_to_pose(location.x, location.y, 0.4, M_PI, 0, 0);
    target_pose6 = list_to_pose(location.x, location.y, block.height + 0.14, M_PI, 0, 0);

    //go_to_pose_goal(arm_interface, target_pose1); // 블록 잡는 곳 중간위치로 이동
    initial_pose(arm_interface);
    go_to_pose_goal(arm_interface, target_pose2); // 블록 잡는 곳 위로 이동
    release_block(gripper_interface);
    go_to_pose_goal(arm_interface, target_pose3); // 블록 잡는 곳으로 이동
    grab_block(gripper_interface, value);
    ros::WallDuration(0.5).sleep();
    go_to_pose_goal(arm_interface, target_pose2); // 블록 잡고 위로 이동
    go_to_pose_goal(arm_interface, target_pose4); // 블록 놓을 곳 중간 위치로 이동
    go_to_pose_goal(arm_interface, target_pose5); // 블록 놓을 곳 위로 이동
    go_to_pose_goal(arm_interface, target_pose6);// 블록 놓을 곳으로 이동
    release_block(gripper_interface);
    ros::WallDuration(0.5).sleep();
    go_to_pose_goal(arm_interface, target_pose5);
}

void p_n_p(moveit::planning_interface::MoveGroupInterface& arm_interface, moveit::planning_interface::MoveGroupInterface& gripper_interface)
{

    Block block[8];
    block[0] = Block(0.05, 0.05, 0.06, 0, Location(0.2, 0.1));
    block[1] = Block(0.05, 0.05, 0.06, 0, Location(0.2, 0.0));
    block[2] = Block(0.05, 0.025, 0.06, 0, Location(0.2, -0.1));
    block[3] = Block(0.05, 0.05, 0.08, 0, Location(0.3, 0.1));
    block[4] = Block(0.05, 0.05, 0.06, 0, Location(0.3, 0.0));
    block[5] = Block(0.05, 0.05, 0.07, 0, Location(0.3, -0.1));
    block[6] = Block(0.05, 0.05, 0.06, 0, Location(0.4, 0.1));
    block[7] = Block(0.05, 0.05, 0.09, 0, Location(0.4, 0.0));

    for(int i = 0; i < 8; i++){
        block[i].location.x += 0.2;
    }

    Location target_location[8];
    target_location[0] = Location(-0.15, 0.35);
    target_location[1] = Location(-0.15, 0.25);
    target_location[2] = Location(0.15, 0.25);
    target_location[3] = Location(0.05, 0.35);
    target_location[4] = Location(-0.05, 0.25);
    target_location[5] = Location(-0.05, 0.35);
    target_location[6] = Location(0.05, 0.25);
    target_location[7] = Location(0.15, 0.35);

    for(int i = 0; i < 8; i++){
        target_location[i].y += 0.2;
    }

    //move_block(arm_interface, gripper_interface, block[6], target_location[6], 0.3);
    // 36이면 잘 잡음
    // move_block(arm_interface, gripper_interface, block[1], target_location[1], 0.36);
    // move_block(arm_interface, gripper_interface, block[4], target_location[4], 0.36);
    // move_block(arm_interface, gripper_interface, block[2], target_location[2], 0.60);
    // move_block(arm_interface, gripper_interface, block[7], target_location[7], 0.36);
    // move_block(arm_interface, gripper_interface, block[5], target_location[5], 0.36);
    // move_block(arm_interface, gripper_interface, block[3], target_location[3], 0.36);
    // move_block(arm_interface, gripper_interface, block[0], target_location[0], 0.36);

    move_block(arm_interface, gripper_interface, block[1], target_location[1], 0.36);
    move_block(arm_interface, gripper_interface, block[4], target_location[4], 0.36);
    move_block(arm_interface, gripper_interface, block[6], target_location[6], 0.45);
    move_block(arm_interface, gripper_interface, block[2], target_location[2], 0.60);
    move_block(arm_interface, gripper_interface, block[7], target_location[7], 0.36);
    move_block(arm_interface, gripper_interface, block[3], target_location[3], 0.36);
    move_block(arm_interface, gripper_interface, block[5], target_location[5], 0.36);
    move_block(arm_interface, gripper_interface, block[0], target_location[0], 0.36);
    
}

void add_ground_plane(moveit::planning_interface::PlanningSceneInterface& planning_scene_interface) {
    moveit_msgs::CollisionObject ground;
    ground.header.frame_id = "link0";  // 로봇의 베이스 프레임에 맞게 조정

    ground.id = "ground_plane";

    shape_msgs::SolidPrimitive ground_box;
    ground_box.type = ground_box.BOX;
    ground_box.dimensions.resize(3);
    ground_box.dimensions[0] = 4.0;  // x 길이
    ground_box.dimensions[1] = 4.0;  // y 길이
    ground_box.dimensions[2] = 0.01; // 두께

    geometry_msgs::Pose ground_pose;
    ground_pose.orientation.w = 1.0;
    ground_pose.position.x = 0.0;
    ground_pose.position.y = 0.0;
    ground_pose.position.z = -0.005;  // 바닥의 중심이 z=0 아래에 위치하도록 (두께 절반만큼)

    ground.primitives.push_back(ground_box);
    ground.primitive_poses.push_back(ground_pose);
    ground.operation = ground.ADD;

    planning_scene_interface.applyCollisionObjects({ground});
}

int main(int argc, char** argv)
{

    ros::init(argc, argv, "rp_midterm");
    ros::NodeHandle nh;
    ros::AsyncSpinner spinner(1);
    spinner.start();

    ros::WallDuration(1.0).sleep();

    moveit::planning_interface::MoveGroupInterface arm("manipulator");
    moveit::planning_interface::MoveGroupInterface gripper("gripper");
    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;
    arm.setPlanningTime(10.0);

    add_ground_plane(planning_scene_interface);

    // Wait a bit for ROS things to initialize
    ros::WallDuration(1.0).sleep();

    p_n_p(arm, gripper);    // execute p_n_p

    return 0;
}

