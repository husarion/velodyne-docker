# Copyright 2024 Husarion sp. z o.o.
# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Launch the velodyne driver, pointcloud, and laserscan nodes with default configuration."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from nav2_common.launch import ReplaceString


def generate_launch_description():
    device_namespace = LaunchConfiguration("device_namespace")
    declare_device_namespace_arg = DeclareLaunchArgument(
        "device_namespace",
        default_value="velodyne",
        description="Namespace for the device, utilized in TF frames and preceding device topics. This aids in differentiating between multiple devices on the same robot.",
    )

    driver_params_file = LaunchConfiguration("driver_params_file")
    declare_driver_params_file_arg = DeclareLaunchArgument(
        "driver_params_file",
        default_value="/config/panther_velodyne_driver.yaml",
        description="Path to the parameter file for the velodyne_driver_node node.",
    )

    robot_namespace = LaunchConfiguration("robot_namespace")
    declare_robot_namespace_arg = DeclareLaunchArgument(
        "robot_namespace",
        default_value=EnvironmentVariable("ROBOT_NAMESPACE", default_value=""),
        description="Namespace to all launched nodes and use namespace as tf_prefix. This aids in differentiating between multiple robots with the same devices.",
    )

    transform_params_file = LaunchConfiguration("transform_params_file")
    declare_transform_params_file_arg = DeclareLaunchArgument(
        "transform_params_file",
        default_value="/config/panther_velodyne_pointcloud.yaml",
        description="Path to the parameter file for the velodyne_transform_node node.",
    )

    x = LaunchConfiguration("x")
    declare_x_arg = DeclareLaunchArgument(
        "x", default_value="0.185", description="Initial robot position in the global 'x' axis."
    )

    y = LaunchConfiguration("y")
    declare_y_arg = DeclareLaunchArgument(
        "y", default_value="0.0", description="Initial robot position in the global 'y' axis."
    )

    z = LaunchConfiguration("z")
    declare_z_arg = DeclareLaunchArgument(
        "z", default_value="0.209", description="Initial robot position in the global 'z' axis."
    )

    roll = LaunchConfiguration("roll")
    declare_roll_arg = DeclareLaunchArgument(
        "roll", default_value="0.0", description="Initial robot 'roll' orientation."
    )

    pitch = LaunchConfiguration("pitch")
    declare_pitch_arg = DeclareLaunchArgument(
        "pitch", default_value="0.0", description="Initial robot 'pitch' orientation."
    )

    yaw = LaunchConfiguration("yaw")
    declare_yaw_arg = DeclareLaunchArgument(
        "yaw", default_value="0.0", description="Initial robot 'yaw' orientation."
    )

    device_ns = PythonExpression(
        ["'", device_namespace, "' + '/' if '", device_namespace, "' else ''"]
    )
    robot_ns = PythonExpression(
        ["'", robot_namespace, "' + '/' if '", robot_namespace, "' else ''"]
    )

    driver_params_file = ReplaceString(
        source_file=driver_params_file,
        replacements={
            "<robot_namespace>/": robot_ns,
            "<device_namespace>": device_namespace,
        },
    )

    velodyne_driver_node = Node(
        package="velodyne_driver",
        executable="velodyne_driver_node",
        parameters=[driver_params_file],
        namespace=robot_namespace,
        remappings=[
            ("velodyne_packets", [device_ns, "velodyne_packets"]),
        ],
    )

    velodyne_transform_node = Node(
        package="velodyne_pointcloud",
        executable="velodyne_transform_node",
        parameters=[transform_params_file],
        namespace=robot_namespace,
        remappings=[
            ("velodyne_packets", [device_ns, "velodyne_packets"]),
            ("velodyne_points", [device_ns, "velodyne_points"]),
        ],
    )

    laserscan_params_file = PathJoinSubstitution(
        [
            FindPackageShare("velodyne_laserscan"),
            "config",
            "default-velodyne_laserscan_node-params.yaml",
        ]
    )

    velodyne_laserscan_node = Node(
        package="velodyne_laserscan",
        executable="velodyne_laserscan_node",
        parameters=[laserscan_params_file],
        namespace=robot_namespace,
        remappings=[
            ("velodyne_points", [device_ns, "velodyne_points"]),
            ("scan", [device_ns, "scan"]),
        ],
    )

    static_transform_publisher = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        namespace=robot_namespace,
        arguments=[
            x,
            y,
            z,
            roll,
            pitch,
            yaw,
            [robot_ns, "cover_link"],
            [robot_ns, device_namespace],
        ],
    )

    return LaunchDescription(
        [
            declare_driver_params_file_arg,
            declare_device_namespace_arg,
            declare_robot_namespace_arg,
            declare_transform_params_file_arg,
            declare_x_arg,
            declare_y_arg,
            declare_z_arg,
            declare_roll_arg,
            declare_pitch_arg,
            declare_yaw_arg,
            velodyne_driver_node,
            velodyne_transform_node,
            velodyne_laserscan_node,
            static_transform_publisher,
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=velodyne_driver_node,
                    on_exit=[EmitEvent(event=Shutdown())],
                )
            ),
        ]
    )
