import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    package_dir = get_package_share_directory(
        'my_robot_description'
    )

    urdf_file = os.path.join(
        package_dir,
        'urdf',
        'my_robot.urdf'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity',
            'my_robot',
            '-file',
            urdf_file
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_robot
    ])
