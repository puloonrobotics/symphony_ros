import sys
import rospy
import moveit_commander
import moveit_msgs.msg
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import tf.transformations as tf
import math
from shape_msgs.msg import SolidPrimitive
import geometry_msgs
import threading
import std_msgs


# Initialize Moveit
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('panda_pick_place', anonymous=True)

# Define the MoveIt interfaces
manipulator_group = moveit_commander.MoveGroupCommander("manipulator")
gripper_group = moveit_commander.MoveGroupCommander("gripper")
scene = moveit_commander.PlanningSceneInterface()

manipulator_group.set_planning_time(25.0)
gripper_group.set_planning_time(10.0)

manipulator_group.set_max_velocity_scaling_factor(0.6)  # 속도 스케일링
manipulator_group.set_max_acceleration_scaling_factor(0.6)  # 가속도 스케일링

gripper_group.set_max_velocity_scaling_factor(0.9)  # 속도 스케일링
gripper_group.set_max_acceleration_scaling_factor(0.9)  # 가속도 스케일링

robot = moveit_commander.RobotCommander()

def update_robot_state():
    ##############################################
    # /rviz/moveit/update_goal_state 토픽에 메시지를 발행하도록 설정
    # std_msgs.msg.Empty() 타입의 빈 메시지를 주기적으로 발행하여 RViz가 goal state를 업데이트하도록 트리거
    # 중요! : Rviz 에서 External comm 을 체크해줘야함.
    ##############################################
    rate = rospy.Rate(5)  # 10 Hz
    update_pub = rospy.Publisher('/rviz/moveit/update_goal_state', std_msgs.msg.Empty, queue_size=10)
    while not rospy.is_shutdown():
        update_pub.publish(std_msgs.msg.Empty())
        rate.sleep()

def open_gripper():
    print("Gripper active joints:", gripper_group.get_active_joints())
    print("Gripper current joint values:", gripper_group.get_current_joint_values())
    gripper_group.set_joint_value_target({"robotiq_85_left_knuckle_joint": 0.0})  # Open position
    gripper_group.go(wait=True)

def close_gripper():
    print("Gripper active joints:", gripper_group.get_active_joints())
    print("Gripper current joint values:", gripper_group.get_current_joint_values())
    gripper_group.set_joint_value_target({"robotiq_85_left_knuckle_joint": 0.6})  # Closed position
    gripper_group.go(wait=True)

def initial():
    manipulator_group.set_joint_value_target({"joint0" : 0.0, "joint1": -2.03, "joint2" : 1.58, "joint3" : -1.19, "joint4" : -1.58, "joint5" : 0.0})
    manipulator_group.go(wait=True)

def pick():
    # 1. Pre-grasp pose 정의
    pre_grasp_pose = geometry_msgs.msg.Pose()
    pre_grasp_pose.position.x = 0.575
    pre_grasp_pose.position.y = 0.0
    pre_grasp_pose.position.z = 0.8
    # quaternion = tf.quaternion_from_euler(-math.pi / 2, -math.pi, -math.pi / 2)
    # quaternion = tf.quaternion_from_euler(-math.pi / 2, 0, -math.pi / 2)
    # pre_grasp_pose.orientation.x = quaternion[0]
    # pre_grasp_pose.orientation.y = quaternion[1]
    # pre_grasp_pose.orientation.z = quaternion[2]
    # pre_grasp_pose.orientation.w = quaternion[3]
    pre_grasp_pose.orientation.x = 0.5
    pre_grasp_pose.orientation.y = 0.5
    pre_grasp_pose.orientation.z = 0.5
    pre_grasp_pose.orientation.w = 0.5

    # 2. Grasp pose 정의
    grasp_pose = geometry_msgs.msg.Pose()
    grasp_pose.position.x = 0.575
    grasp_pose.position.y = 0.0
    grasp_pose.position.z = 0.58  # 물체 높이에 맞게 조정
    # grasp_pose.orientation.x = quaternion[0]
    # grasp_pose.orientation.y = quaternion[1]
    # grasp_pose.orientation.z = quaternion[2]
    # grasp_pose.orientation.w = quaternion[3]
    grasp_pose.orientation.x = pre_grasp_pose.orientation.x
    grasp_pose.orientation.y = pre_grasp_pose.orientation.y
    grasp_pose.orientation.z = pre_grasp_pose.orientation.z
    grasp_pose.orientation.w = pre_grasp_pose.orientation.w

    # 3. Post-grasp pose 정의 (후퇴 위치)
    post_grasp_pose = geometry_msgs.msg.Pose()
    post_grasp_pose.position.x = 0.575
    post_grasp_pose.position.y = 0.0
    post_grasp_pose.position.z = 0.8
    # quaternion = tf.quaternion_from_euler(math.pi / 2, 0, math.pi)
    # post_grasp_pose.orientation.x = quaternion[0]
    # post_grasp_pose.orientation.y = quaternion[1]
    # post_grasp_pose.orientation.z = quaternion[2]
    # post_grasp_pose.orientation.w = quaternion[3]
    post_grasp_pose.orientation.x = pre_grasp_pose.orientation.x
    post_grasp_pose.orientation.y = pre_grasp_pose.orientation.y
    post_grasp_pose.orientation.z = pre_grasp_pose.orientation.z
    post_grasp_pose.orientation.w = pre_grasp_pose.orientation.w

    manipulator_group.set_start_state_to_current_state()

    print("============A=============")
    # Pre-grasp pose로 이동 (팔 제어)
    manipulator_group.set_pose_target(pre_grasp_pose)
    manipulator_group.go(wait=True)
    print("============B=============")
    # Gripper 열기
    open_gripper()
    print("============C=============")
    # Grasp pose로 이동 (팔 제어)
    manipulator_group.set_pose_target(grasp_pose)
    manipulator_group.go(wait=True)
    print("============D=============")
    # Gripper 닫기 (물체 잡기)
    close_gripper()
    print("============E=============")
    # 플래닝 씬 업데이트 (물체가 로봇에 붙음)
    scene.attach_box("link6", "object", touch_links=["robotiq_85_left_knuckle_joint"])
    print("============F=============")
    # Post-grasp pose로 이동 (팔 제어)
    manipulator_group.set_pose_target(post_grasp_pose)
    manipulator_group.go(wait=True)
    print("============G=============")

# Define the place function
def place():
    # 1. Place pose 정의 (물체를 놓을 위치)
    
    place_pose = geometry_msgs.msg.Pose()
    place_pose.position.x = 0.0
    place_pose.position.y = 0.6
    place_pose.position.z = 0.58  # 테이블 위 높이
    # quaternion = tf.quaternion_from_euler(0, 0, math.pi / 2)
    # quaternion = tf.quaternion_from_euler(math.pi / 2, 0, math.pi)
    # quaternion = tf.quaternion_from_euler(math.pi / 2, math.pi, math.pi)
    quaternion = tf.quaternion_from_euler(math.pi / 2, 0, -math.pi)
    place_pose.orientation.x = quaternion[0]
    place_pose.orientation.y = quaternion[1]
    place_pose.orientation.z = quaternion[2]
    place_pose.orientation.w = quaternion[3]

    # 2. Pre-place pose 정의 (접근 위치)
    pre_place_pose = geometry_msgs.msg.Pose()
    pre_place_pose.position.x = 0.0
    pre_place_pose.position.y = 0.6
    pre_place_pose.position.z = 0.65  # 약간 위에서 접근
    pre_place_pose.orientation.x = place_pose.orientation.x
    pre_place_pose.orientation.y = place_pose.orientation.y
    pre_place_pose.orientation.z = place_pose.orientation.z
    pre_place_pose.orientation.w = place_pose.orientation.w

    # 3. Post-place pose 정의 (후퇴 위치)
    post_place_pose = geometry_msgs.msg.Pose()
    post_place_pose.position.x = 0.0
    post_place_pose.position.y = 0.5
    post_place_pose.position.z = 0.6  # 약간 위로 후퇴
    post_place_pose.orientation.x = place_pose.orientation.x
    post_place_pose.orientation.y = place_pose.orientation.y
    post_place_pose.orientation.z = place_pose.orientation.z
    post_place_pose.orientation.w = place_pose.orientation.w

    manipulator_group.set_start_state_to_current_state()

    print("============H=============")
    # Pre-place pose로 이동 (팔 제어)
    manipulator_group.set_pose_target(pre_place_pose)
    manipulator_group.go(wait=True)
    print("============I=============")
    # Place pose로 이동 (팔 제어)
    manipulator_group.set_pose_target(place_pose)
    manipulator_group.go(wait=True)
    print("============J=============")
    # Gripper 열기 (물체 놓기)
    open_gripper()
    print("============K=============")
    # 플래닝 씬 업데이트 (물체를 테이블에 놓음)
    scene.remove_attached_object("link6", name="object")
    print("============L=============")
    # Post-place pose로 이동 (팔 제어)
    manipulator_group.set_pose_target(post_place_pose)
    manipulator_group.go(wait=True)
    print("============M=============")


# Define the function to add collision objects
def add_collision_objects():
    # Define the first table
    table1 = moveit_msgs.msg.CollisionObject()
    table1.id = "table1"
    table1.header.frame_id = "link0"
    # table1.primitives.append(moveit_msgs.msg.SolidPrimitive())
    # table1.primitives[0].type = moveit_msgs.msg.SolidPrimitive.BOX
    table1.primitives.append(SolidPrimitive())
    table1.primitives[0].type = SolidPrimitive.BOX
    table1.primitives[0].dimensions = [0.2, 0.4, 0.4]
    table1.primitive_poses.append(PoseStamped().pose)
    table1.primitive_poses[0].position.x = 0.7
    table1.primitive_poses[0].position.y = 0.0
    table1.primitive_poses[0].position.z = 0.2
    table1.operation = moveit_msgs.msg.CollisionObject.ADD

    # Define the second table
    table2 = moveit_msgs.msg.CollisionObject()
    table2.id = "table2"
    table2.header.frame_id = "link0"
    # table2.primitives.append(moveit_msgs.msg.SolidPrimitive())
    # table2.primitives[0].type = moveit_msgs.msg.SolidPrimitive.BOX
    table2.primitives.append(SolidPrimitive())
    table2.primitives[0].type = SolidPrimitive.BOX
    table2.primitives[0].dimensions = [0.4, 0.2, 0.4]
    table2.primitive_poses.append(PoseStamped().pose)
    table2.primitive_poses[0].position.x = 0.0
    table2.primitive_poses[0].position.y = 0.7
    table2.primitive_poses[0].position.z = 0.2
    table2.operation = moveit_msgs.msg.CollisionObject.ADD

    # define obstacle
    obstacle = moveit_msgs.msg.CollisionObject()
    obstacle.id = "obstacle"
    obstacle.header.frame_id = "link0"
    obstacle.primitives.append(SolidPrimitive())
    obstacle.primitives[0].type = SolidPrimitive.BOX
    obstacle.primitives[0].dimensions = [0.2, 0.2, 0.2]
    obstacle.primitive_poses.append(PoseStamped().pose)
    obstacle.primitive_poses[0].position.x = 0.4
    obstacle.primitive_poses[0].position.y = 0.4
    obstacle.primitive_poses[0].position.z = 0.55
    obstacle.operation = moveit_msgs.msg.CollisionObject.ADD

    # Define the object
    object_to_pick = moveit_msgs.msg.CollisionObject()
    object_to_pick.id = "object"
    object_to_pick.header.frame_id = "link0"
    # object_to_pick.primitives.append(moveit_msgs.msg.SolidPrimitive())
    # object_to_pick.primitives[0].type = moveit_msgs.msg.SolidPrimitive.BOX
    object_to_pick.primitives.append(SolidPrimitive())
    object_to_pick.primitives[0].type = SolidPrimitive.BOX
    object_to_pick.primitives[0].dimensions = [0.02, 0.02, 0.2]
    object_to_pick.primitive_poses.append(PoseStamped().pose)
    object_to_pick.primitive_poses[0].position.x = 0.7
    object_to_pick.primitive_poses[0].position.y = 0.0
    object_to_pick.primitive_poses[0].position.z = 0.5
    object_to_pick.operation = moveit_msgs.msg.CollisionObject.ADD

    scene.add_object(table1)
    scene.add_object(table2)
    scene.add_object(obstacle)
    scene.add_object(object_to_pick)

if __name__ == "__main__":

    state_update_thread = threading.Thread(target=update_robot_state)
    state_update_thread.daemon = True
    state_update_thread.start()

    rospy.sleep(1)
    initial()
    rospy.sleep(1)
    add_collision_objects()
    rospy.sleep(1)
    pick()
    rospy.sleep(1)
    place()
    rospy.spin()
