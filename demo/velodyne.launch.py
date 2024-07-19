#!/usr/bin/env python3

# Copyright 2024 Husarion sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import EnvironmentVariable, LaunchConfiguration
from launch_ros.actions import Node


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

    velodyne_driver = Node(
        package="velodyne_driver",
        executable="velodyne_driver_node",
        name=device_namespace,
        namespace=robot_namespace,
        parameters=[
            {
                "frame_id": device_namespace,
                "tf_prefix": robot_namespace,
            },
        ],
    )

    velodyne_pointcloud = Node(
        package="velodyne_driver",
        executable="velodyne_driver",
        name=device_namespace,
        namespace=robot_namespace,
        parameters=[
            {
                "frame_id": device_namespace,
                "tf_prefix": robot_namespace,
            },
        ],
    )

    return LaunchDescription(
        [
            declare_robot_namespace_arg,
            declare_device_namespace_arg,
            velodyne_driver,
            velodyne_pointcloud
        ]
    )
