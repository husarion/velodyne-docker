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

import os

import ament_index_python.packages
import launch
import launch_ros.actions

from launch.actions import DeclareLaunchArgument
from launch.substitutions import EnvironmentVariable, LaunchConfiguration
from nav2_common.launch import ReplaceString


def generate_launch_description():
    device_namespace = LaunchConfiguration("device_namespace")
    declare_device_namespace_arg = DeclareLaunchArgument(
        "device_namespace",
        default_value="velodyne",
        description="Namespace for the device, utilized in TF frames and preceding device topics. This aids in differentiating between multiple cameras on the same robot.",
    )

    robot_namespace = LaunchConfiguration("robot_namespace")
    declare_robot_namespace_arg = DeclareLaunchArgument(
        "robot_namespace",
        default_value=EnvironmentVariable("ROBOT_NAMESPACE", default_value=""),
        description="Namespace to all launched nodes and use namespace as tf_prefix. This aids in differentiating between multiple robots with the same devices.",
    )

    driver_params_file = LaunchConfiguration("driver_params_file")
    driver_params_file_arg = DeclareLaunchArgument(
        "driver_params_file",
        default_value="/config/driver_params_file.yaml",
        description="Path to the parameter file for the velodyne_driver_node node.",
    )

    transform_params_file = LaunchConfiguration("transform_params_file")
    transform_params_file_arg = DeclareLaunchArgument(
        "transform_params_file",
        default_value="/config/transform_params_file.yaml",
        description="Path to the parameter file for the velodyne_transform_node node.",
    )

    driver_params_file = ReplaceString(
        source_file=driver_params_file,
        replacements={"<robot_namespace>": robot_namespace, "//": "/"},
    )
    driver_params_file = ReplaceString(
        source_file=driver_params_file,
        replacements={"<device_namespace>": device_namespace},
    )

    velodyne_driver_node = launch_ros.actions.Node(
        package="velodyne_driver",
        executable="velodyne_driver_node",
        output="both",
        parameters=[driver_params_file],
        namespace=robot_namespace,
        remappings=[
            ("velodyne_packets", [device_namespace, "/velodyne_packets"]),
        ],
    )

    velodyne_transform_node = launch_ros.actions.Node(
        package="velodyne_pointcloud",
        executable="velodyne_transform_node",
        output="both",
        parameters=[transform_params_file],
        namespace=robot_namespace,
        remappings=[
            ("velodyne_packets", [device_namespace, "/velodyne_packets"]),
            ("velodyne_points", [device_namespace, "/velodyne_points"]),
        ],
    )

    laserscan_share_dir = ament_index_python.packages.get_package_share_directory(
        "velodyne_laserscan"
    )
    laserscan_params_file = os.path.join(
        laserscan_share_dir, "config", "default-velodyne_laserscan_node-params.yaml"
    )
    velodyne_laserscan_node = launch_ros.actions.Node(
        package="velodyne_laserscan",
        executable="velodyne_laserscan_node",
        output="both",
        parameters=[laserscan_params_file],
        namespace=robot_namespace,
        remappings=[
            ("velodyne_points", [device_namespace, "/velodyne_points"]),
            ("scan", [device_namespace, "/scan"]),
        ],
    )

    return launch.LaunchDescription(
        [
            driver_params_file_arg,
            transform_params_file_arg,
            declare_device_namespace_arg,
            declare_robot_namespace_arg,
            velodyne_driver_node,
            velodyne_transform_node,
            velodyne_laserscan_node,
            launch.actions.RegisterEventHandler(
                event_handler=launch.event_handlers.OnProcessExit(
                    target_action=velodyne_driver_node,
                    on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
                )
            ),
        ]
    )
