import sys
import rospy
import moveit_commander
import moveit_msgs.msg
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import tf.transformations as tf
import math
from shape_msgs.msg import SolidPrimitive


# Initialize Moveit
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('panda_pick_place', anonymous=True)

# Define the MoveIt interfaces
manipulator_group = moveit_commander.MoveGroupCommander("manipulator")
scene = moveit_commander.PlanningSceneInterface()

manipulator_group.set_planning_time(45.0)

def open_gripper(posture):
    posture.joint_names = ["robotiq_85_left_knuckle_joint"]
    point = JointTrajectoryPoint()
    point.positions = [0.035]
    point.time_from_start = rospy.Duration(0.5)
    posture.points = [point]

def close_gripper(posture):
    posture.joint_names = ["robotiq_85_left_knuckle_joint"]
    point = JointTrajectoryPoint()
    point.positions = [0.0]
    point.time_from_start = rospy.Duration(0.5)
    posture.points = [point]

def pick():
    grasps = []
    grasp = moveit_msgs.msg.Grasp()
    grasp.grasp_pose.header.frame_id = "link0"
    quaternion = tf.quaternion_from_euler(-math.pi / 2, -math.pi / 4, -math.pi / 2)
    # quaternion = tf.quaternion_from_euler(-math.pi / 2, 0, -math.pi / 2)
    grasp.grasp_pose.pose.orientation.x = quaternion[0]
    grasp.grasp_pose.pose.orientation.y = quaternion[1]
    grasp.grasp_pose.pose.orientation.z = quaternion[2]
    grasp.grasp_pose.pose.orientation.w = quaternion[3]
    # grasp.grasp_pose.pose.position.x = 0.415
    grasp.grasp_pose.pose.position.x = 0.385
    grasp.grasp_pose.pose.position.y = 0.0
    grasp.grasp_pose.pose.position.z = 0.5
    # Pre-grasp approach
    grasp.pre_grasp_approach.direction.header.frame_id = "link0"
    grasp.pre_grasp_approach.direction.vector.x = 1.0
    # grasp.pre_grasp_approach.min_distance = 0.095
    grasp.pre_grasp_approach.min_distance = 0.1
    # grasp.pre_grasp_approach.desired_distance = 0.115
    grasp.pre_grasp_approach.desired_distance = 0.15
    # Post-grasp retreat
    grasp.post_grasp_retreat.direction.header.frame_id = "link0"
    grasp.post_grasp_retreat.direction.vector.z = 1.0
    grasp.post_grasp_retreat.min_distance = 0.1
    grasp.post_grasp_retreat.desired_distance = 0.25

    # Open gripper for pre-grasp
    open_gripper(grasp.pre_grasp_posture)

    # Close gripper for grasp
    close_gripper(grasp.grasp_posture)

    grasps.append(grasp)
    manipulator_group.set_support_surface_name("table1")
    manipulator_group.pick("object", grasps)

# Define the place function
def place():
    place_location = moveit_msgs.msg.PlaceLocation()

    place_location.place_pose.header.frame_id = "link0"
    quaternion = tf.quaternion_from_euler(0, 0, math.pi / 2)
    place_location.place_pose.pose.orientation.x = quaternion[0]
    place_location.place_pose.pose.orientation.y = quaternion[1]
    place_location.place_pose.pose.orientation.z = quaternion[2]
    place_location.place_pose.pose.orientation.w = quaternion[3]
    place_location.place_pose.pose.position.x = 0.0
    place_location.place_pose.pose.position.y = 0.5
    place_location.place_pose.pose.position.z = 0.5

    # Pre-place approach
    place_location.pre_place_approach.direction.header.frame_id = "link0"
    place_location.pre_place_approach.direction.vector.z = -1.0
    place_location.pre_place_approach.min_distance = 0.095
    place_location.pre_place_approach.desired_distance = 0.115

    # Post-place retreat
    place_location.post_place_retreat.direction.header.frame_id = "link0"
    place_location.post_place_retreat.direction.vector.y = -1.0
    place_location.post_place_retreat.min_distance = 0.1
    place_location.post_place_retreat.desired_distance = 0.25

    # Open gripper after placing
    open_gripper(place_location.post_place_posture)
    # open_gripper()

    manipulator_group.set_support_surface_name("table2")
    manipulator_group.place("object", [place_location])






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
    table1.primitive_poses[0].position.x = 0.5
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
    table2.primitive_poses[0].position.y = 0.5
    table2.primitive_poses[0].position.z = 0.2
    table2.operation = moveit_msgs.msg.CollisionObject.ADD

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
    object_to_pick.primitive_poses[0].position.x = 0.5
    object_to_pick.primitive_poses[0].position.y = 0.0
    object_to_pick.primitive_poses[0].position.z = 0.5
    object_to_pick.operation = moveit_msgs.msg.CollisionObject.ADD

    scene.add_object(table1)
    scene.add_object(table2)
    scene.add_object(object_to_pick)

if __name__ == "__main__":
    rospy.sleep(1)
    add_collision_objects()
    rospy.sleep(1)
    pick()
    rospy.sleep(1)
    place()
    rospy.spin()
