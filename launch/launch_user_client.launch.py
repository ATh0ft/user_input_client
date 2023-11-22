from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='user_input_client',
            executable='client',
            output='screen'),
    ])
