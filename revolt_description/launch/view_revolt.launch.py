import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import xacro

def generate_launch_description():

    # Arguments
    rviz_argument = DeclareLaunchArgument('rviz', default_value='true',
                          description='Open RViz.')
    rsp_argument = DeclareLaunchArgument('rsp', default_value='true',
                          description='Run robot state publisher node.')
    jsp_argument = DeclareLaunchArgument('jsp', default_value='true',
                          description='Run joint state publisher node.')

    # Obtains revolt_description's share directory path.
    pkg_revolt_description = get_package_share_directory('revolt_description')

    # Obtain urdf from xacro files.
    arguments = {'yaml_config_dir': os.path.join(pkg_revolt_description, 'config', 'revolt')}
    doc = xacro.process_file(os.path.join(pkg_revolt_description, 'urdf', 'revolt.urdf.xacro'), mappings = arguments)
    robot_desc = doc.toprettyxml(indent='  ')
    params = {'robot_description': robot_desc,
              'publish_frequency': 30.0}

    # Robot state publisher
    rsp = Node(package='robot_state_publisher',
                executable='robot_state_publisher',
                namespace='',
                output='both',
                parameters=[params],
                condition=IfCondition(LaunchConfiguration('rsp'))
    )

    # Joint state publisher gui
    jsp_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        namespace='',
        name='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('jsp'))
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_revolt_description, 'rviz', 'revolt_description.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    return LaunchDescription([
        jsp_argument,
        rviz_argument,
        rsp_argument,
        jsp_gui,
        rviz,
        rsp,
    ])