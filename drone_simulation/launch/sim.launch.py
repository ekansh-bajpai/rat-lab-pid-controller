from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Start Gazebo with the drone world
    gazebo = ExecuteProcess(
        cmd=[
            "gz", "sim", "-v", "4",
            os.path.join(get_package_share_directory('drone_simulation'), "models/drone_world.sdf")
        ],
        output="screen"
    )

    # ROS-Gazebo bridge (delayed 3s to let Gazebo fully start)
    ros_gz_bridge = TimerAction(
        period=3.0,
        actions=[
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                name="ros_gz_bridge",
                output="screen",
                arguments=[
                    "/X3/gazebo/command/motor_speed@actuator_msgs/msg/Actuators@gz.msgs.Actuators",
                    "/world/quadcopter/pose/info@geometry_msgs/msg/PoseArray@gz.msgs.Pose_V"
                ]
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        ros_gz_bridge,
    ])