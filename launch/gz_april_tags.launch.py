from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from pathlib import Path
import os


def generate_launch_description():
    apriltag_pkg_share = get_package_share_directory("gazebo_apriltag")

    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[
            str(Path(apriltag_pkg_share).parent.resolve())
        ]
    )

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py"),
        launch_arguments={'gz_args': [
            '-r -v4 ', 'empty.sdf'], 'on_exit_shutdown': 'true'}.items()
    )

    gz_spawn_entity_tag_0 = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-file", f"{apriltag_pkg_share}/models/Apriltag36_11_00000/model.sdf",
                   "-name", "tag_0",
                   '-x', '0.0',
                   '-y', '0.0',
                   '-z', '0.1'],
    )

    return LaunchDescription([
        gazebo_resource_path,
        gazebo,
        gz_spawn_entity_tag_0,
    ])
